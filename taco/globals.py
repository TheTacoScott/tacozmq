import threading
import taco.constants
import logging
import os
settings_lock  = threading.Lock()
settings = {}

chat_log = []
chat_log_lock = threading.Lock()

continue_running_lock = threading.Lock()
continue_running_value = True

public_keys_lock = threading.Lock()
public_keys = {}

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
  os._exit(3)

