import threading
import logging
import time
import zmq
import taco.globals
import taco.constants
import taco.commands
import os
import socket
import random
import msgpack

class TacoServer(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop = threading.Event() 

    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1
    
    self.client_last_request_time = {}
    self.client_last_request_time_lock = threading.Lock()

  def set_client_last_request(self,peer_uuid):
    #self.set_status("Server has serviced a request from:" + peer_uuid)
    with self.client_last_request_time_lock:
      self.client_last_request_time[peer_uuid] = time.time()

  def get_client_last_request(self,peer_uuid):
    with self.client_last_request_time_lock:
      if peer_uuid in self.client_last_request_time:
        return self.client_last_request_time[peer_uuid]
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

  def run(self):
    self.set_status("Server Startup")
    
    self.set_status("Creating zmq Contexts",1)
    serverctx = zmq.Context() 
    
    self.set_status("Starting zmq ThreadedAuthenticator",1)
    serverauth = zmq.auth.ThreadedAuthenticator(serverctx)
    serverauth.start()
    
    with taco.globals.settings_lock:
      bindip     = taco.globals.settings["Application IP"]
      bindport   = taco.globals.settings["Application Port"]
      localuuid  = taco.globals.settings["Local UUID"]
      publicdir  = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/public/"))
      privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/"  + taco.globals.settings["Local UUID"] + "/private/"))

    self.set_status("Configuring Curve to use publickey dir:" + publicdir)
    serverauth.configure_curve(domain='*', location=publicdir)
    #auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)

    self.set_status("Creating Server Context",1)
    server = serverctx.socket(zmq.REP)
    server.setsockopt(zmq.LINGER, 0)

    self.set_status("Loading Server Certs",1)
    server_public, server_secret = zmq.auth.load_certificate(os.path.normpath(os.path.abspath(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX +"-server.key_secret")))
    server.curve_secretkey = server_secret
    server.curve_publickey = server_public
   
    server.curve_server = True
    if bindip == "0.0.0.0": bindip ="*"
    self.set_status("Server is now listening for encrypted ZMQ connections @ "+ "tcp://" + bindip +":" + str(bindport)) 
    server.bind("tcp://" + bindip +":" + str(bindport))
    
    poller = zmq.Poller()
    poller.register(server, zmq.POLLIN|zmq.POLLOUT)

    while not self.stop.is_set():
      socks = dict(poller.poll(200))
      if server in socks and socks[server] == zmq.POLLIN:
        self.set_status("Getting a request")
        data = server.recv()
        with taco.globals.download_limiter_lock: taco.globals.download_limiter.add(len(data))
        (client_uuid,reply) = taco.commands.Proccess_Request(data)
        if client_uuid!="0": self.set_client_last_request(client_uuid)
      socks = dict(poller.poll(10))
      if server in socks and socks[server] == zmq.POLLOUT:
        self.set_status("Replying to a request")
        with taco.globals.upload_limiter_lock: taco.globals.upload_limiter.add(len(reply))
        server.send(reply)

        


    self.set_status("Stopping zmq server with 0 second linger")
    server.close(0)
    self.set_status("Stopping zmq ThreadedAuthenticator")
    serverauth.stop() 
    serverctx.term()
    self.set_status("Server Exit")    
