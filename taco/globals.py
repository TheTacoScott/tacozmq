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

chat_uuid = uuid.uuid4().hex
chat_uuid_lock = threading.Lock()

stop = threading.Event()

public_keys_lock = threading.Lock()
public_keys = {}

share_listings_i_care_about = {}
share_listings_i_care_about_lock = threading.Lock()

share_listing_requests_lock = threading.Lock()
share_listing_requests = {}

share_listings = {}
share_listings_lock = threading.Lock()

download_q = {}
download_q_lock = threading.Lock()

upload_q = {}
upload_q_lock = threading.Lock()

upload_limiter_lock = threading.Lock()
download_limiter_lock = threading.Lock()

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
        return 1
  elif priority==2:
    with medium_priority_output_queue_lock:
      if medium_priority_output_queue.has_key(peer_uuid):
        medium_priority_output_queue[peer_uuid].put(msg)
        return 1
  else:
    with low_priority_output_queue_lock:
      if low_priority_output_queue.has_key(peer_uuid):
        low_priority_output_queue[peer_uuid].put(msg)
        return 1
  taco.globals.filesys.sleep.clear()
  return 0

def Add_To_All_Output_Queues(msg,priority=3):
  logging.debug("Add to ALL output q @ " + str(priority))
  if priority==1:
    with high_priority_output_queue_lock:
      for keyname in high_priority_output_queue.keys():
        high_priority_output_queue[keyname].put(msg)
      return 1
  elif priority==2:
    with medium_priority_output_queue_lock:
      for keyname in medium_priority_output_queue.keys():
        medium_priority_output_queue[keyname].put(msg)
      return 1
  else:
    with low_priority_output_queue_lock:
      for keyname in low_priority_output_queue.keys():
        low_priority_output_queue[keyname].put(msg)
      return 1
  taco.globals.filesys.sleep.clear()
  return 0



def properexit(signum, frame):
  logging.warning("SIGINT Detected, stopping TacoNET")
  stop.set()
  logging.info("Stopping Server")
  server.stop.set()
  logging.info("Stopping Clients")
  clients.stop.set()
  logging.info("Stopping Filesystem Workers")
  filesys.stop.set()
  server.join()
  clients.join()
  filesys.join()
  logging.info("Dispatcher Stopped Successfully")
  logging.info("Clean Exit")
  os._exit(3)

