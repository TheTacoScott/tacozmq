import taco.globals
import taco.constants

import os
import logging
import zmq.auth
import shutil
import re

def Init_Local_Crypto():
  logging.debug("Started")
  with taco.globals.settings_lock:
    workingdir = taco.globals.settings["TacoNET Certificates Store"]
    privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/private"))
    publicdir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/public"))
  if not os.path.isdir(privatedir): os.makedirs(privatedir)
  if not os.path.isdir(publicdir): os.makedirs(publicdir)

  server_generate = False
  if not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,taco.constants.KEY_GENERATION_PREFIX + "-server.key")))) or not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,taco.constants.KEY_GENERATION_PREFIX + "-server.key_secret")))): 
    server_generate = True

  client_generate = False
  if not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,taco.constants.KEY_GENERATION_PREFIX + "-client.key")))) or not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,taco.constants.KEY_GENERATION_PREFIX + "-client.key_secret")))): 
    client_generate = True

  if server_generate:
    logging.info("Server CURVE Public or Private Key Missing, Generating")
    server_public_file, server_secret_file = zmq.auth.create_certificates(workingdir, taco.constants.KEY_GENERATION_PREFIX + "-server")
    shutil.move(os.path.normpath(os.path.abspath(server_public_file)),os.path.normpath(os.path.abspath(privatedir)))
    shutil.move(os.path.normpath(os.path.abspath(server_secret_file)),os.path.normpath(os.path.abspath(privatedir)))
  if client_generate:
    logging.info("Client CURVE Public or Private Key Missing, Generating")
    client_public_file, client_secret_file = zmq.auth.create_certificates(workingdir, taco.constants.KEY_GENERATION_PREFIX + "-client")
    shutil.move(os.path.normpath(os.path.abspath(client_public_file)),os.path.normpath(os.path.abspath(privatedir)))
    shutil.move(os.path.normpath(os.path.abspath(client_secret_file)),os.path.normpath(os.path.abspath(privatedir)))

  logging.debug("Getting keys into globals")

  with taco.globals.settings_lock:
    workingdir = taco.globals.settings["TacoNET Certificates Store"]
    privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/private"))
  client_public_key = s = open(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX + "-client.key", 'r').read()
  server_public_key = s = open(privatedir + "/" + taco.constants.KEY_GENERATION_PREFIX + "-server.key", 'r').read()
  with taco.globals.public_keys_lock:
    data = re.search(r'.*public-key = "(.*)"',client_public_key ,re.MULTILINE)
    if (data): taco.globals.public_keys["client"] = data.group(1)
    data = re.search(r'.*public-key = "(.*)"',server_public_key ,re.MULTILINE)
    if (data): taco.globals.public_keys["server"] = data.group(1)
  
  logging.debug("Finished")

