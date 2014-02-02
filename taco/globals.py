import threading
import taco.constants

json_file_settings_lock = threading.Lock()

settings_lock  = threading.Lock()
settings = {}

peers_lock  = threading.Lock()
peers = {}

shares_lock = threading.Lock()
shares = []

chat_log = []
chat_log_lock = threading.Lock()

continue_running_lock = threading.Lock()
continue_running_value = True

def continue_running():
    return_value = True
    with taco.globals.continue_running_lock:
        return_value = taco.globals.continue_running_value
    return return_value
    
def stop_running():
    with taco.globals.continue_running_lock:
        taco.globals.continue_running_value = False
