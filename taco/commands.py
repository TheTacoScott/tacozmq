import taco.globals
import taco.constants
import msgpack
import logging

def Proccess_Request(packed):
  response = {taco.constants.NET_GARBAGE:taco.constants.NET_GARBAGE,taco.constants.NET_DATABLOCK:""}
  try:
    unpacked = msgpack.unpackb(packed)
    assert unpacked.has_key(taco.constants.NET_DATABLOCK)
  except:
    return response
  #logging.debug("Processing Request:" + str(unpacked))
  if unpacked.has_key(taco.constants.NET_REQUEST):
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_ROLLCALL: return Response_Rollcall()
  
  return response

def Request_Rollcall():
  request = {taco.constants.NET_REQUEST:taco.constants.NET_REQUEST_ROLLCALL,taco.constants.NET_DATABLOCK:""}
  return msgpack.packb(request)

def Response_Rollcall():
  with taco.globals.settings_lock:
    response = {taco.constants.NET_REPLY:taco.constants.NET_REPLY_ROLLCALL,taco.constants.NET_DATABLOCK:[taco.globals.settings["Local UUID"]] + taco.globals.settings["Peers"].keys()}
  return msgpack.packb(response)
  
