import threading
import logging
import time
import zmq
import taco.globals
import taco.constants
import os
import socket

class TacoDispatch(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop_lock = threading.Lock()     
    self.stop = False
    
    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1

    self.client_connect_time = time.time()
    self.clients = {}
    self.did_something = False

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
    self.set_status("Dispatcher Startup")
    
    self.set_status("Creating zmq Context",1)
    ctx = zmq.Context().instance() 
    
    self.set_status("Starting zmq ThreadedAuthenticator",1)
    auth = zmq.auth.ThreadedAuthenticator(ctx)
    auth.start()
    
    with taco.globals.settings_lock:
      bindip     = taco.globals.settings["Application IP"]
      bindport   = taco.globals.settings["Application Port"] 
      publicdir  = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/public/"))
      privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/private/"))

    self.set_status("Configuring Curve to use publickey dir:" + publicdir)
    auth.configure_curve(domain='*', location=publicdir)

    self.set_status("Creating Server Context",1)
    server = ctx.socket(zmq.ROUTER)
    server.setsockopt(zmq.LINGER, 1)

    self.set_status("Loading Server Certs",1)
    server_public, server_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-server.key_secret")))
    server.curve_secretkey = server_secret
    server.curve_publickey = server_public
   
    self.set_status("Server is now listening for encrypted ZMQ connections") 
    server.bind("tcp://" + bindip +":" + str(bindport))

    self.set_status("Starting zmq Poller")
    serverpoller = zmq.Poller()
    serverpoller.register(server,zmq.POLLIN|zmq.POLLOUT)
  
    clientpoller = zmq.Poller()

    while self.continue_running():
      if not self.continue_running(): break
      if not self.did_something: 
        time.sleep(0.05) 
      else: 
        self.did_something = False

      socks = dict(serverpoller.poll())
      if server in socks and socks[server] == zmq.POLLIN:
        pass
      if server in socks and socks[server] == zmq.POLLOUT:
        pass
      socks = dict(clientpoller.poll())
      for peer_uuid in self.clients.keys():
        if self.clients[peer_uuid] in socks:
          if socks[self.clients[peer_uuid]] == zmq.POLLIN:
            pass
          if socks[self.clients[peer_uuid]] == zmq.POLLOUT:
            pass

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
                self.clients[peer_uuid] = ctx.socket(zmq.DEALER)
                self.clients[peer_uuid].setsockopt(zmq.LINGER, 0)
                client_public, client_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-client.key_secret")))
                self.clients[peer_uuid].curve_secretkey = client_secret
                self.clients[peer_uuid].curve_publickey = client_public
                self.clients[peer_uuid].curve_serverkey = str(taco.globals.settings["Peers"][peer_uuid]["serverkey"])
                self.set_status("Attempt to connect to client: " + peer_uuid + " @ tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                self.clients[peer_uuid].connect("tcp://" + ip_of_client + ":" + str(taco.globals.settings["Peers"][peer_uuid]["port"]))
                clientpoller.register(self.clients[peer_uuid],zmq.POLLIN|zmq.POLLOUT)

    self.set_status("Stopping zmq server with 1 second linger")
    server.close(1)
    for client in self.clients.keys():
      self.set_status("Stopping zmq client with 0 second linger: " + client)
      self.clients[client].close(0)             
    self.set_status("Stopping zmq ThreadedAuthenticator")
    auth.stop() 
    ctx.term()
    self.set_status("Dispatcher Exit")    
