import taco.globals
import taco.constants
import taco.defaults
import os
import json
import logging

def Load_Settings():
  logging.debug("Started")
  save_after = False

  with taco.globals.settings_lock:
    try:
      logging.debug("Loading Settings JSON")
      taco.globals.settings = json.loads(open(taco.constants.JSON_SETTINGS_FILENAME,'r').read())
    except:
      taco.globals.settings = {}
      taco.globals.settings["Peers"] = {}
      taco.globals.settings["Shares"] = []

    logging.debug("Verifying the settings loaded from the json isn't missing any required keys")
    for keyname in taco.defaults.default_settings_kv.keys():
      if not taco.globals.settings.has_key(keyname):
        taco.globals.settings[keyname] =  taco.defaults.default_settings_kv[keyname]
        save_after = True

    if not os.path.isdir(taco.globals.settings["Curve Temp Location"]): 
      logging.debug("Making CURVE Working Directory")
      os.makedirs(taco.globals.settings["Curve Temp Location"])
    if not os.path.isdir(taco.globals.settings["Curve Private Location"]): 
      logging.debug("Making CURVE Private Directory")
      os.makedirs(taco.globals.settings["Curve Private Location"])
    if not os.path.isdir(taco.globals.settings["Curve Public Location"]): 
      logging.debug("Making CURVE Public Directory")
      os.makedirs(taco.globals.settings["Curve Public Location"])

    logging.debug("Verifying settings share list is in correct format")
    valid_list = False
    for value in taco.globals.settings["Shares"]:
      if type(value) == type([]):
        if len(value) == 2: 
          (sharename,shareloc) = value
          if type(sharename) == type(shareloc) == type(unicode("test")): 
            valid_list = True
      if not valid_list:       
        taco.globals.shares = []
        save_after = True

    logging.debug("Verifying settings peer dict is in correct format")
    for peer_uuid in taco.globals.settings["Peers"].keys():
      for keyname in taco.defaults.default_peers_kv.keys():
        taco.globals.settings["Peers"][peer_uuid][keyname] = taco.defaults.default_peers_kv[keyname]
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
