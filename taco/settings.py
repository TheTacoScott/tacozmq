import taco.globals
import taco.constants
import taco.defaults
import os
import json
import logging

def Load_Settings(needlock=True):
  logging.debug("Started")
  save_after = False
  if needlock: taco.globals.settings_lock.acquire()

  try:
    logging.debug("Loading Settings JSON")
    taco.globals.settings = json.loads(open(taco.constants.JSON_SETTINGS_FILENAME,'r').read())
  except:
    taco.globals.settings = {}
    taco.globals.settings["Peers"] = {}
    taco.globals.settings["Shares"] = {}

  logging.debug("Verifying the settings loaded from the json isn't missing any required keys")
  for keyname in taco.defaults.default_settings_kv.keys():
    if not taco.globals.settings.has_key(keyname):
      taco.globals.settings[keyname] =  taco.defaults.default_settings_kv[keyname]
      save_after = True

  if not os.path.isdir(taco.globals.settings["TacoNET Certificates Store"]): 
    logging.debug("Making TacoNET Certificates Store")
    os.makedirs(taco.globals.settings["TacoNET Certificates Store"])

  logging.debug("Verifying settings share list is in correct format")
  valid_list = False
  if type(taco.globals.settings["Shares"]) == type([]):
    valid_list = True

  if not valid_list:       
    taco.globals.shares = []
    save_after = True

  logging.debug("Verifying settings peer dict is in correct format")
  for peer_uuid in taco.globals.settings["Peers"].keys():
    for keyname in taco.defaults.default_peers_kv.keys():
      taco.globals.settings["Peers"][peer_uuid][keyname] = taco.defaults.default_peers_kv[keyname]
      save_after = True
  
  if needlock: taco.globals.settings_lock.release()

  if save_after:
    logging.info("Settings need to be saved")
    Save_Settings()
  logging.debug("Finished")

def Save_Settings(needlock=True):
  logging.debug("Started")
  if needlock: taco.globals.settings_lock.acquire()
  open(taco.constants.JSON_SETTINGS_FILENAME,'w').write(json.dumps(taco.globals.settings,indent=4,sort_keys=True))
  if needlock: taco.globals.settings_lock.release()
  Load_Settings(needlock)
  logging.debug("Finished")
