import threading
import taco.constants
import logging
import os
import uuid
import Queue

settings_lock  = threading.Lock()
settings = {}

chat_log = []
chat_log_lock = threading.Lock()

chat_uuid = str(uuid.uuid4())
chat_uuid_lock = threading.Lock()

continue_running_lock = threading.Lock()
continue_running_value = True

public_keys_lock = threading.Lock()
public_keys = {}

share_listings_i_care_about = {}
share_listings_i_care_about_lock = threading.Lock()

share_listing_requests_lock = threading.Lock()
share_listing_requests = {}

share_listings = {}
share_listings_lock = threading.Lock()

def continue_running():
  return_value = True
  with taco.globals.continue_running_lock:
    return_value = taco.globals.continue_running_value
  return return_value
    
def stop_running():
  with taco.globals.continue_running_lock:
    taco.globals.continue_running_value = False

def properexit(signum, frame):
  logging.warning("SIGINT Detected, stopping TacoNET")
  stop_running()
  logging.info("Stopping Server")
  server.stop_running()
  logging.info("Stopping Clients")
  clients.stop_running()
  logging.info("Stopping Filesystem Workers")
  filesys.stop_running()
  server.join()
  clients.join()
  filesys.join()
  logging.info("Dispatcher Stopped Successfully")
  logging.info("Clean Exit")
  os._exit(3)

