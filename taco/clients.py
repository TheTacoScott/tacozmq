import threading
import logging
import time
import zmq
import taco.globals
import taco.constants
import taco.commands
import os
import Queue
import socket
import random
import msgpack

class TacoClients(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop_lock = threading.Lock()     
    self.stop = False
    
    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1
    self.next_request = ""

    self.clients = {}
    self.long_clients = {}
    self.short_clients = {}

    self.next_rollcall = {}
    self.client_connect_time = -1
    
    self.output_queues = {}
    self.output_queues_lock = threading.Lock()
 
    self.client_last_reply_time = {}
    self.client_last_reply_time_lock = threading.Lock()

  def Add_To_All_Output_Queues(self,msg):
    with self.output_queues_lock:
      for keyname in self.output_queues.keys():
         self.output_queues[keyname].put(msg)
  
  def set_client_last_reply(self,peer_uuid):
    with self.client_last_reply_time_lock:
      self.client_last_reply_time[peer_uuid] = time.time()

  def get_client_last_reply(self,peer_uuid):
    with self.client_last_reply_time_lock:
      if self.client_last_reply_time.has_key(peer_uuid):
        return self.client_last_reply_time[peer_uuid]
    return -1
  
  def set_status(self,text,level=0):
    if   level==0: logging.info(text)
    elif level==1: logging.debug(text)
    with self.status_lock:
      self.status = text
      self.status_time = time.time()
  
  def get_status(self):
    with self.status_lock:
      return (self.status,self.status_time)     

  def stop_running(self):
    with self.stop_lock:
      self.stop = True

  def continue_running(self):
    with self.stop_lock:
      continue_run = not self.stop
    return continue_run

  def run(self):
    self.set_status("Client Startup")
    self.set_status("Creating zmq Contexts",1)
    clientctx = zmq.Context() 
    self.set_status("Starting zmq ThreadedAuthenticator",1)
    clientauth = zmq.auth.ThreadedAuthenticator(clientctx)
    clientauth.start()
    
    with taco.globals.settings_lock:
      localuuid  = taco.globals.settings["Local UUID"]
      publicdir  = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/public/"))
      privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/private/"))

    self.set_status("Configuring Curve to use publickey dir:" + publicdir)
    clientauth.configure_curve(domain='*', location=publicdir)
    
    poller = zmq.Poller()

    while self.continue_running():
      #logging.debug("client")
      if not self.continue_running(): break

      if self.client_connect_time < time.time():
        self.set_status("Checking if dispatch needs to connect to clients")
        self.client_connect_time = time.time() + taco.constants.CLIENT_RECONNECT
        with taco.globals.settings_lock:
          for peer_uuid in taco.globals.settings["Peers"].keys():
            if taco.globals.settings["Peers"][peer_uuid]["enabled"]:
              if peer_uuid not in self.clients:
                self.set_status("Doing DNS lookup on: " + taco.globals.settings["Peers"][peer_uuid]["hostname"])
                ip_of_client = socket.gethostbyname(taco.globals.settings["Peers"][peer_uuid]["hostname"])

                self.set_status("Creating client zmq context for: " + peer_uuid)
                self.clients[peer_uuid] = clientctx.socket(zmq.REQ)
                self.clients[peer_uuid].setsockopt(zmq.LINGER, 0)
                client_public, client_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-client.key_secret")))
                self.clients[peer_uuid].curve_secretkey = client_secret
                self.clients[peer_uuid].curve_publickey = client_public
                self.clients[peer_uuid].curve_serverkey = str(taco.globals.settings["Peers"][peer_uuid]["serverkey"])

                self.set_status("Attempt to connect to client: " + peer_uuid + " @ tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                self.clients[peer_uuid].connect("tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                self.next_rollcall[peer_uuid] = time.time()
                with self.output_queues_lock:
                  self.output_queues[peer_uuid] = Queue.Queue()
                self.set_client_last_reply(peer_uuid)
                poller.register(self.clients[peer_uuid],zmq.POLLIN|zmq.POLLOUT)

      socks = dict(poller.poll(500))
      if len(self.clients.keys()) == 0: time.sleep(0.5)
      self.did_something = 0
      for peer_uuid in self.clients.keys():

        #SEND BLOCK 
        if self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLOUT:
          if self.next_request != "":
            self.clients[peer_uuid].send(self.next_request)
            self.did_something = 1
            self.next_request = ""
            continue
          
          with self.output_queues_lock:
            if not self.output_queues[peer_uuid].empty():
              data = msgpack.unpackb(self.output_queues[peer_uuid].get())
              logging.debug("output q not empty:" + peer_uuid + " : " + str(data))
              self.clients[peer_uuid].send(msgpack.packb(data))
              self.did_something = 1
              continue

          if self.next_rollcall[peer_uuid] < time.time():
            logging.debug("Requesting Rollcall from: " + peer_uuid)
            self.clients[peer_uuid].send(taco.commands.Request_Rollcall())
            self.did_something = 1
            self.next_rollcall[peer_uuid] = time.time() + random.randint(taco.constants.ROLLCALL_MIN,taco.constants.ROLLCALL_MAX)
            continue

        #RECEIVE BLOCK
        if self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLIN:
          data = self.clients[peer_uuid].recv()
          self.set_client_last_reply(peer_uuid)
          self.did_something = 1
          self.next_request = taco.commands.Process_Reply(peer_uuid,data)

        #cleanup block
        if self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLERR:
          logging.debug("got a socket error for:" + peer_uuid)
          poller.unregister(self.clients[peer_uuid])
          self.clients[peer_uuid].close(0)
          del self.clients[peer_uuid]          
          with self.output_queues_lock:
            del self.output_queues[peer_uuid]
          
        if abs(self.get_client_last_reply(peer_uuid) - time.time()) > taco.constants.ROLLCALL_TIMEOUT:
          logging.debug("Stopping client since I havn't heard from: " + peer_uuid)
          poller.unregister(self.clients[peer_uuid])
          self.clients[peer_uuid].close(0)
          del self.clients[peer_uuid]          
          with self.output_queues_lock:
            del self.output_queues[peer_uuid]
      if not self.did_something: time.sleep(0.2)
            
          

        
    self.set_status("Terminating Clients")
    for peer_uuid in self.clients.keys():
      self.clients[peer_uuid].close(0)
    self.set_status("Stopping zmq ThreadedAuthenticator")
    clientauth.stop() 
    clientctx.term()
    self.set_status("Clients Exit")    
