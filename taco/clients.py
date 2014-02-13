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
    self.client_connect_time = {}
    self.client_reconnect_mod = {}
 
    self.high_priority_output_queue = {}
    self.high_priority_output_queue_lock = threading.Lock()

    self.medium_priority_output_queue = {}
    self.medium_priority_output_queue_lock = threading.Lock()

    self.low_priority_output_queue = {}
    self.low_priority_output_queue_lock = threading.Lock()
 
 
    self.client_last_reply_time = {}
    self.client_last_reply_time_lock = threading.Lock()

    self.client_timeout = {}
  def Add_To_Output_Queue(self,peer_uuid,msg,priority=3):
    logging.debug("Add to output q @ " + str(priority))
    if priority==1:
      with self.high_priority_output_queue_lock:
        if self.high_priority_output_queue.has_key(peer_uuid):
          self.high_priority_output_queue[peer_uuid].put(msg)
    elif priority==2:
      with self.medium_priority_output_queue_lock:
        if self.medium_priority_output_queue.has_key(peer_uuid):
          self.medium_priority_output_queue[peer_uuid].put(msg)
    else:
      with self.low_priority_output_queue_lock:
        if self.low_priority_output_queue.has_key(peer_uuid):
          self.low_priority_output_queue[peer_uuid].put(msg)

  def Add_To_All_Output_Queues(self,msg,priority=3):
    logging.debug("Add to ALL output q @ " + str(priority))
    if priority==1:
      with self.high_priority_output_queue_lock:
        for keyname in self.high_priority_output_queue.keys():
          self.high_priority_output_queue[keyname].put(msg)
    elif priority==2:
      with self.medium_priority_output_queue_lock:
        for keyname in self.medium_priority_output_queue.keys():
          self.medium_priority_output_queue[keyname].put(msg)
    else:
      with self.low_priority_output_queue_lock:
        for keyname in self.low_priority_output_queue.keys():
          self.low_priority_output_queue[keyname].put(msg)

    logging.debug("DONE Add to output q @ " + str(priority))
  
  def set_client_last_reply(self,peer_uuid):
    logging.debug("Got Reply from: " + peer_uuid)
    self.client_reconnect_mod[peer_uuid] = taco.constants.CLIENT_RECONNECT_MIN
    self.client_timeout[peer_uuid] = time.time() + taco.constants.ROLLCALL_TIMEOUT
    with self.client_last_reply_time_lock:
      self.client_last_reply_time[peer_uuid] = time.time()

  def get_client_last_reply(self,peer_uuid):
    with self.client_last_reply_time_lock:
      if self.client_last_reply_time.has_key(peer_uuid):
        return self.client_last_reply_time[peer_uuid]
    return -1
  
  def set_status(self,text,level=0):
    if   level==1: logging.info(text)
    elif level==0: logging.debug(text)
    elif level==2: logging.warning(text)
    elif level==3: logging.error(text)
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

      with taco.globals.settings_lock:
        for peer_uuid in taco.globals.settings["Peers"].keys():
          if taco.globals.settings["Peers"][peer_uuid]["enabled"]:
            #init some defaults
            if not self.client_reconnect_mod.has_key(peer_uuid): self.client_reconnect_mod[peer_uuid] = taco.constants.CLIENT_RECONNECT_MIN
            if not self.client_connect_time.has_key(peer_uuid): self.client_connect_time[peer_uuid] = time.time() + self.client_reconnect_mod[peer_uuid]
            if not self.client_timeout.has_key(peer_uuid): self.client_timeout[peer_uuid] = time.time() + taco.constants.ROLLCALL_TIMEOUT

            if time.time() >= self.client_connect_time[peer_uuid]:
              if peer_uuid not in self.clients.keys():
                self.set_status("Starting Client for: " + peer_uuid)
                self.set_status("Doing DNS lookup on: " + taco.globals.settings["Peers"][peer_uuid]["hostname"])
                ip_of_client = socket.gethostbyname(taco.globals.settings["Peers"][peer_uuid]["hostname"])

                self.set_status("Creating client zmq context for: " + peer_uuid)
                self.clients[peer_uuid] = clientctx.socket(zmq.REQ)
                self.clients[peer_uuid].setsockopt(zmq.LINGER, 0)
                client_public, client_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-client.key_secret")))
                self.clients[peer_uuid].curve_secretkey = client_secret
                self.clients[peer_uuid].curve_publickey = client_public
                self.clients[peer_uuid].curve_serverkey = str(taco.globals.settings["Peers"][peer_uuid]["serverkey"])

                self.set_status("Attempt to connect to: " + peer_uuid + " @ tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                self.clients[peer_uuid].connect("tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                self.next_rollcall[peer_uuid] = time.time()

                with self.high_priority_output_queue_lock: self.high_priority_output_queue[peer_uuid] = Queue.Queue()
                with self.medium_priority_output_queue_lock: self.medium_priority_output_queue[peer_uuid] = Queue.Queue()
                with self.low_priority_output_queue_lock: self.low_priority_output_queue[peer_uuid] = Queue.Queue()

                poller.register(self.clients[peer_uuid],zmq.POLLIN|zmq.POLLOUT)

      socks = dict(poller.poll(500))
      if len(self.clients.keys()) == 0: time.sleep(0.5)
      self.did_something = 0
      for peer_uuid in self.clients.keys():

        #SEND BLOCK 
        if self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLOUT:
          
          #high priority queue processing
          with self.high_priority_output_queue_lock:
            if not self.high_priority_output_queue[peer_uuid].empty():
              data = self.high_priority_output_queue[peer_uuid].get()
              self.set_status("high priority output q not empty:" + peer_uuid)
              self.clients[peer_uuid].send(data)
              self.did_something = 1
              continue

          #medium priority queue processing
          with self.medium_priority_output_queue_lock:
            if not self.medium_priority_output_queue[peer_uuid].empty():
              data = self.medium_priority_output_queue[peer_uuid].get()
              self.set_status("medium priority output q not empty:" + peer_uuid)
              self.clients[peer_uuid].send(data)
              self.did_something = 1
              continue

          #low priority queue processing
          with self.low_priority_output_queue_lock:
            if not self.low_priority_output_queue[peer_uuid].empty():
              data = self.low_priority_output_queue[peer_uuid].get()
              self.set_status("low priority output q not empty:" + peer_uuid)
              self.clients[peer_uuid].send(data)
              self.did_something = 1
              continue

          #rollcall special case
          if self.next_rollcall[peer_uuid] < time.time():
            self.set_status("Requesting Rollcall from: " + peer_uuid)
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
          if self.next_request != "":
            with self.medium_priority_output_queue_lock:
              self.medium_priority_output_queue[peer_uuid].put(self.next_request)

        #cleanup block
        self.error_msg = []
        if self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLERR: self.error_msg.append("got a socket error")
        if abs(self.client_timeout[peer_uuid] - time.time()) > taco.constants.ROLLCALL_TIMEOUT: self.error_msg.append("havn't seen communications")

        if len(self.error_msg) > 0:
          self.set_status("Stopping client: " + peer_uuid + " -- " + " and ".join(self.error_msg),2)
          poller.unregister(self.clients[peer_uuid])
          self.clients[peer_uuid].close(0)
          del self.clients[peer_uuid]          
          del self.client_timeout[peer_uuid]
          with self.high_priority_output_queue_lock: del self.high_priority_output_queue[peer_uuid]
          with self.medium_priority_output_queue_lock: del self.medium_priority_output_queue[peer_uuid]
          with self.low_priority_output_queue_lock: del self.low_priority_output_queue[peer_uuid]
          self.client_reconnect_mod[peer_uuid] = min(self.client_reconnect_mod[peer_uuid] + taco.constants.CLIENT_RECONNECT_MOD,taco.constants.CLIENT_RECONNECT_MAX)
          self.client_connect_time[peer_uuid] = time.time() + self.client_reconnect_mod[peer_uuid]
          

      if not self.did_something: time.sleep(0.2)
            
          

        
    self.set_status("Terminating Clients")
    for peer_uuid in self.clients.keys():
      self.clients[peer_uuid].close(0)
    self.set_status("Stopping zmq ThreadedAuthenticator")
    clientauth.stop() 
    clientctx.term()
    self.set_status("Clients Exit")    
