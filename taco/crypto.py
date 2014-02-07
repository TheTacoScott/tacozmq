import taco.globals
import os
import logging
import zmq.auth
import shutil

def Init_Local_Crypto():
  logging.debug("Started")
  with taco.globals.settings_lock:
    workingdir = taco.globals.settings["TacoNET Certificates Store"]
    privatedir = os.path.normpath(os.path.abspath(taco.globals.settings["TacoNET Certificates Store"] + "/private"))
  if not os.path.isdir(privatedir): os.makedirs(privatedir)

  server_generate = False
  if not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,"taconet-server.key")))) or not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,"taconet-server.key_secret")))): 
    server_generate = True

  client_generate = False
  if not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,"taconet-client.key")))) or not os.path.isfile(os.path.abspath(os.path.normpath(os.path.join(privatedir,"taconet-client.key_secret")))): 
    client_generate = True

  if server_generate:
    logging.info("Server CURVE Public or Private Key Missing, Generating")
    server_public_file, server_secret_file = zmq.auth.create_certificates(workingdir, "taconet-server")
    shutil.move(os.path.normpath(os.path.abspath(server_public_file)),os.path.normpath(os.path.abspath(privatedir)))
    shutil.move(os.path.normpath(os.path.abspath(server_secret_file)),os.path.normpath(os.path.abspath(privatedir)))
  if client_generate:
    logging.info("Client CURVE Public or Private Key Missing, Generating")
    client_public_file, client_secret_file = zmq.auth.create_certificates(workingdir, "taconet-client")
    shutil.move(os.path.normpath(os.path.abspath(client_public_file)),os.path.normpath(os.path.abspath(privatedir)))
    shutil.move(os.path.normpath(os.path.abspath(client_secret_file)),os.path.normpath(os.path.abspath(privatedir)))

  logging.debug("Finished")
