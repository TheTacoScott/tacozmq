import taco.globals
import taco.constants
import json
import uuid
import logging

def Load_Settings():
  logging.debug("Started")
  save_after = False

  default_settings_kv = {}
  default_settings_kv["Download Location"] = "/tmp"
  default_settings_kv["Network Password"] = "Some password here"
  default_settings_kv["Download Location"] = "/tmp"
  default_settings_kv["Nickname"] = "Your Nickname Here"
  default_settings_kv["Application Port"] = 9001
  default_settings_kv["Application IP"] = "0.0.0.0"
  default_settings_kv["Web Port"] = 9002
  default_settings_kv["Web IP"] = "127.0.0.1"
  default_settings_kv["External Port"] = 9001
  default_settings_kv["External IP"] = "127.0.0.1"
  default_settings_kv["Download Limit"] = 50
  default_settings_kv["Upload Limit"] = 50
  default_settings_kv["Local UUID"] = unicode(str(uuid.uuid4()))

  default_peers_kv = {}
  default_peers_kv["Enabled"] = False
  default_peers_kv["Hostname"] = "127.0.0.1"
  default_peers_kv["Port"] = "9001"
  default_peers_kv["Nickname Local"] = "Local Nickname"
  default_peers_kv["Nickname Remote"] = "Remote Nickname"
  default_peers_kv["Broadcast"] = True
  default_peers_kv["Dynamic"] = False
  
  with taco.globals.settings_lock:
    try:
      #load setting json
      taco.globals.settings = json.loads(open(taco.constants.JSON_SETTINGS_FILENAME,'r').read())
    except:
      taco.globals.settings = {}
      taco.globals.settings["Peers"] = {}
      taco.globals.settings["Shares"] = []

    #verify it has all keys, and correct missing ones
    for keyname in default_settings_kv.keys():
      if not taco.globals.settings.has_key(keyname):
        taco.globals.settings[keyname] = default_settings_kv[keyname]
        save_after = True

    #verify share list is in good shape
    valid_list = False
    for value in taco.globals.settings["Shares"]:
      #confirm the share loaded from the json is a list
      if type(value) == type([]): #must be a list
        if len(value[0]) == 2: #each item in the list must be a tuple
          (sharename,shareloc) = value[0]
          if type(sharename) == type(shareloc) == type(unicode("test")): #sharename and location are unicode strings
            valid_list = True
      if not valid_list:       
        taco.globals.shares = []
        save_after = True

    for peer_uuid in taco.globals.settings["Peers"].keys():
      for keyname in default_peers_kv.keys():
        taco.globals.settings["Peers"][peer_uuid][keyname] = default_peers_kv[keyname]
        save_after = True

  if save_after:
    logging.info("Settings need to be saved")
    Save_Settings()
  logging.debug("Finished")

def Save_Settings():
  logging.debug("Started")
  with taco.globals.settings_lock:
    open(taco.constants.JSON_SETTINGS_FILENAME,'w').write(json.dumps(taco.globals.settings,indent=4,sort_keys=True))
  Load_Settings()
  logging.debug("Finished")
