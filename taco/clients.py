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

    self.stop  = threading.Event() 
    self.sleep = threading.Event() 
    
    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1
    self.next_request = ""

    self.clients = {}

    self.next_rollcall = {}
    self.client_connect_time = {}
    self.client_reconnect_mod = {}
 
    self.client_last_reply_time = {}
    self.client_last_reply_time_lock = threading.Lock()

    self.client_timeout = {}

    self.connect_block_time = 0
    
  def set_client_last_reply(self,peer_uuid):
    #logging.debug("Got Reply from: " + peer_uuid)
    self.client_reconnect_mod[peer_uuid] = taco.constants.CLIENT_RECONNECT_MIN
    self.client_timeout[peer_uuid] = time.time() + taco.constants.ROLLCALL_TIMEOUT
    with self.client_last_reply_time_lock:
      self.client_last_reply_time[peer_uuid] = time.time()

  def get_client_last_reply(self,peer_uuid):
    with self.client_last_reply_time_lock:
      if peer_uuid in self.client_last_reply_time:
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
    while not self.stop.is_set():
      #logging.debug("PRE")
      result = self.sleep.wait(0.2)
      #logging.debug(result)
      self.sleep.clear()
      if self.stop.is_set(): break

      if abs(time.time() - self.connect_block_time) > 1:
        self.connect_block_time = time.time() 
        with taco.globals.settings_lock:
          for peer_uuid in taco.globals.settings["Peers"].keys():
            if taco.globals.settings["Peers"][peer_uuid]["enabled"]:
              #init some defaults
              if not peer_uuid in self.client_reconnect_mod: self.client_reconnect_mod[peer_uuid] = taco.constants.CLIENT_RECONNECT_MIN
              if not peer_uuid in self.client_connect_time:  self.client_connect_time[peer_uuid]  = time.time() + self.client_reconnect_mod[peer_uuid]
              if not peer_uuid in self.client_timeout:       self.client_timeout[peer_uuid]       = time.time() + taco.constants.ROLLCALL_TIMEOUT

              if time.time() >= self.client_connect_time[peer_uuid]:
                if peer_uuid not in self.clients.keys():
                  self.set_status("Starting Client for: " + peer_uuid)
                  ip_of_client = socket.gethostbyname(taco.globals.settings["Peers"][peer_uuid]["hostname"])
                  self.clients[peer_uuid] = clientctx.socket(zmq.DEALER)
                  self.clients[peer_uuid].setsockopt(zmq.LINGER, 0)
                  client_public, client_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-client.key_secret")))
                  self.clients[peer_uuid].curve_secretkey = client_secret
                  self.clients[peer_uuid].curve_publickey = client_public
                  self.clients[peer_uuid].curve_serverkey = str(taco.globals.settings["Peers"][peer_uuid]["serverkey"])
                  self.clients[peer_uuid].connect("tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                  self.next_rollcall[peer_uuid] = time.time()

                  with taco.globals.high_priority_output_queue_lock:   taco.globals.high_priority_output_queue[peer_uuid]   = Queue.Queue()
                  with taco.globals.medium_priority_output_queue_lock: taco.globals.medium_priority_output_queue[peer_uuid] = Queue.Queue()
                  with taco.globals.low_priority_output_queue_lock:    taco.globals.low_priority_output_queue[peer_uuid]    = Queue.Queue()

                  poller.register(self.clients[peer_uuid],zmq.POLLIN)

      if len(self.clients.keys()) == 0: 
        self.set_status("No Active Clients in clients dict")
        continue

      peer_keys = self.clients.keys()
      random.shuffle(peer_keys)
      for peer_uuid in peer_keys:
        #self.set_status("Socket Write Possible:" + peer_uuid)

        #high priority queue processing
        with taco.globals.high_priority_output_queue_lock:
          while not taco.globals.high_priority_output_queue[peer_uuid].empty():
            self.set_status("high priority output q not empty:" + peer_uuid)
            data = taco.globals.high_priority_output_queue[peer_uuid].get()
            self.clients[peer_uuid].send_multipart(['',data])
            self.sleep.set()
            with taco.globals.upload_limiter_lock: taco.globals.upload_limiter.add(len(data))

        #medium priority queue processing
        with taco.globals.medium_priority_output_queue_lock:
          while not taco.globals.medium_priority_output_queue[peer_uuid].empty():
            self.set_status("medium priority output q not empty:" + peer_uuid)
            data = taco.globals.medium_priority_output_queue[peer_uuid].get()
            self.clients[peer_uuid].send_multipart(['',data])
            self.sleep.set()
            with taco.globals.upload_limiter_lock: taco.globals.upload_limiter.add(len(data))

        #low priority queue processing
        with taco.globals.low_priority_output_queue_lock:
          if not taco.globals.low_priority_output_queue[peer_uuid].empty():
            self.set_status("low priority output q not empty:" + peer_uuid)
            data = taco.globals.low_priority_output_queue[peer_uuid].get()
            self.clients[peer_uuid].send_multipart(['',data])
            self.sleep.set()
            with taco.globals.upload_limiter_lock: taco.globals.upload_limiter.add(len(data))
            #continue

        #rollcall special case
        if self.next_rollcall[peer_uuid] < time.time():
          #self.set_status("Requesting Rollcall from: " + peer_uuid)
          data = taco.commands.Request_Rollcall()
          self.clients[peer_uuid].send_multipart(['',data])
          with taco.globals.upload_limiter_lock: taco.globals.upload_limiter.add(len(data))
          self.next_rollcall[peer_uuid] = time.time() + random.randint(taco.constants.ROLLCALL_MIN,taco.constants.ROLLCALL_MAX)
          self.sleep.set()
          #continue

        #RECEIVE BLOCK
        socks = dict(poller.poll(0))
        while self.clients[peer_uuid] in socks and socks[self.clients[peer_uuid]] == zmq.POLLIN:
          #self.set_status("Socket Read Possible")
          sink,data = self.clients[peer_uuid].recv_multipart()
          with taco.globals.download_limiter_lock: taco.globals.download_limiter.add(len(data))
          self.set_client_last_reply(peer_uuid)
          self.next_request = taco.commands.Process_Reply(peer_uuid,data)
          if self.next_request != "":
            with taco.globals.medium_priority_output_queue_lock:
              taco.globals.medium_priority_output_queue[peer_uuid].put(self.next_request)
          self.sleep.set()
          socks = dict(poller.poll(0))

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
          with taco.globals.high_priority_output_queue_lock:    del taco.globals.high_priority_output_queue[peer_uuid]
          with taco.globals.medium_priority_output_queue_lock:  del taco.globals.medium_priority_output_queue[peer_uuid]
          with taco.globals.low_priority_output_queue_lock:     del taco.globals.low_priority_output_queue[peer_uuid]
          self.client_reconnect_mod[peer_uuid] = min(self.client_reconnect_mod[peer_uuid] + taco.constants.CLIENT_RECONNECT_MOD,taco.constants.CLIENT_RECONNECT_MAX)
          self.client_connect_time[peer_uuid] = time.time() + self.client_reconnect_mod[peer_uuid]
          

        
    self.set_status("Terminating Clients")
    for peer_uuid in self.clients.keys():
      self.clients[peer_uuid].close(0)
    self.set_status("Stopping zmq ThreadedAuthenticator")
    clientauth.stop() 
    clientctx.term()
    self.set_status("Clients Exit")    
