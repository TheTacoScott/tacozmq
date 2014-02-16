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

high_priority_output_queue_lock = threading.Lock()
medium_priority_output_queue_lock = threading.Lock()
low_priority_output_queue_lock = threading.Lock()

high_priority_output_queue = {}
medium_priority_output_queue = {}
low_priority_output_queue = {}

def Add_To_Output_Queue(peer_uuid,msg,priority=3):
  logging.debug("Add to "+ peer_uuid+" output q @ " + str(priority))
  if priority==1:
    with high_priority_output_queue_lock:
      if high_priority_output_queue.has_key(peer_uuid):
        high_priority_output_queue[peer_uuid].put(msg)
  elif priority==2:
    with medium_priority_output_queue_lock:
      if medium_priority_output_queue.has_key(peer_uuid):
        medium_priority_output_queue[peer_uuid].put(msg)
  else:
    with low_priority_output_queue_lock:
      if low_priority_output_queue.has_key(peer_uuid):
        low_priority_output_queue[peer_uuid].put(msg)

def Add_To_All_Output_Queues(msg,priority=3):
  logging.debug("Add to ALL output q @ " + str(priority))
  if priority==1:
    with high_priority_output_queue_lock:
      for keyname in high_priority_output_queue.keys():
        high_priority_output_queue[keyname].put(msg)
  elif priority==2:
    with medium_priority_output_queue_lock:
      for keyname in medium_priority_output_queue.keys():
        medium_priority_output_queue[keyname].put(msg)
  else:
    with low_priority_output_queue_lock:
      for keyname in low_priority_output_queue.keys():
        low_priority_output_queue[keyname].put(msg)



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

