import threading
import logging
import time
import zmq
import taco.globals
import taco.constants
import os
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

    self.clients = {}

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


    while self.continue_running():
      if not self.continue_running(): break
      time.sleep(0.5)
        


    self.set_status("Stopping zmq ThreadedAuthenticator")
    clientauth.stop() 
    clientctx.term()
    self.set_status("Clients Exit")    
