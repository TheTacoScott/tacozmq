import threading
import logging
import time
import taco.globals
import taco.constants
import taco.commands
import os
import Queue
import socket
import random
import msgpack

class TacoDownloadq(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop_lock = threading.Lock()     
    self.stop = False
    
    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1

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
    self.set_status("DownloadQ Startup")
    while self.continue_running():
      if not self.continue_running(): break
      time.sleep(random.uniform(0.01, 0.05))

    self.set_status("DownloadQ Exit")
