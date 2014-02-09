import taco.globals
import taco.constants
import taco.defaults
import os
import json
import logging
import time

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
  files_in_pubdir = []
  if os.path.isdir(os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/public/"))):
    files_in_pubdir = os.listdir(os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/public/")))
  print files_in_pubdir
  for peer_uuid in taco.globals.settings["Peers"].keys():
    if taco.globals.settings["Peers"][peer_uuid]["enabled"]:
      Enable_Key(peer_uuid,"client",taco.globals.settings["Peers"][peer_uuid]["clientkey"],False)    
      Enable_Key(peer_uuid,"server",taco.globals.settings["Peers"][peer_uuid]["serverkey"],False)

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

def Enable_Key(peeruuid,keytype,keystring,needlock):
  logging.info("Enabling KEY for UUID:" +peeruuid + " -- " + keytype + " -- " + keystring)
  template = """
#   **** Saved on %s by taconet  ****
#   for peer: %s
#   type: %s
#   ZeroMQ CURVE Public Certificate
#   Exchange securely, or use a secure mechanism to verify the contents
#   of this file after exchange. Store public certificates in your home
#   directory, in the .curve subdirectory.

metadata
curve
    public-key = "%s"
  """
  template_out = template % (str(time.time()),peeruuid,keytype,keystring)

  if needlock: taco.globals.settings_lock.acquire()
  publicdir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/public"))
  location = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/public/" + peeruuid + "-" + keytype + ".key"))
  if needlock: taco.globals.settings_lock.release()

  template_out = template % (str(time.time()),peeruuid,keytype,keystring)
  if not os.path.isdir(publicdir): os.makedirs(publicdir)
  output = open(location, 'w').write(template_out)
