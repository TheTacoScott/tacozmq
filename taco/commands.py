import taco.globals
import taco.constants
import taco.settings
import msgpack
import logging
import time
import uuid

def Proccess_Request(packed):
  response = {taco.constants.NET_GARBAGE:taco.constants.NET_GARBAGE,taco.constants.NET_DATABLOCK:""}
  try:
    unpacked = msgpack.unpackb(packed)
    assert unpacked.has_key(taco.constants.NET_DATABLOCK)
  except:
    return msgpack.packb(response)
  logging.info("NET_REQUEST: " + str(unpacked))
  if unpacked.has_key(taco.constants.NET_REQUEST):
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_ROLLCALL: return Reply_Rollcall()
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_CERTS: return Reply_Certs(unpacked[taco.constants.NET_DATABLOCK])
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_CHAT: return Reply_Chat(unpacked[taco.constants.NET_DATABLOCK])
  
  return msgpack.packb(response)

def Process_Reply(peer_uuid,packed):
  response = ""
  try:
    unpacked = msgpack.unpackb(packed)
    assert unpacked.has_key(taco.constants.NET_DATABLOCK)
  except:
    return response
  if unpacked.has_key(taco.constants.NET_REPLY):
    logging.info("NET_REPLY: " + str(unpacked))
    if unpacked[taco.constants.NET_REPLY] == taco.constants.NET_REPLY_ROLLCALL: return Process_Reply_Rollcall(peer_uuid,unpacked[taco.constants.NET_DATABLOCK])
    if unpacked[taco.constants.NET_REPLY] == taco.constants.NET_REPLY_CERTS: return Process_Reply_Certs(peer_uuid,unpacked[taco.constants.NET_DATABLOCK])

  return response

def Request_Chat(chatmsg):
  with taco.globals.settings_lock:
    output_block = {taco.constants.NET_REQUEST:taco.constants.NET_REQUEST_CHAT,taco.constants.NET_DATABLOCK:[]}
    output_block[taco.constants.NET_DATABLOCK] = [taco.globals.settings["Local UUID"],time.time(),chatmsg]
  with taco.globals.chat_log_lock:
    taco.globals.chat_log.append([taco.globals.settings["Local UUID"],time.time(),chatmsg])
    with taco.globals.chat_uuid_lock:
      taco.globals.chat_uuid = str(uuid.uuid4())
    if len(taco.globals.chat_log) > taco.constants.CHAT_LOG_MAXSIZE:
      taco.globals.chat_log = taco.globals.chat_log[1:]

  taco.globals.clients.Add_To_All_Output_Queues(msgpack.packb(output_block))

def Reply_Chat(datablock):
  logging.debug(str(datablock))
  with taco.globals.chat_log_lock:
    taco.globals.chat_log.append(datablock)
    with taco.globals.chat_uuid_lock:
      taco.globals.chat_uuid = str(uuid.uuid4())
    if len(taco.globals.chat_log) > taco.constants.CHAT_LOG_MAXSIZE:
      taco.globals.chat_log = taco.globals.chat_log[1:]

  response = {taco.constants.NET_REPLY:taco.constants.NET_REPLY_CHAT,taco.constants.NET_DATABLOCK:{}}
  return msgpack.packb(response)

def Request_Rollcall():
  request = {taco.constants.NET_REQUEST:taco.constants.NET_REQUEST_ROLLCALL,taco.constants.NET_DATABLOCK:""}
  return msgpack.packb(request)

def Reply_Rollcall():
  peers_i_can_talk_to = []
  with taco.globals.settings_lock:
    for peer_uuid in taco.globals.settings["Peers"].keys():
      if abs(taco.globals.clients.get_client_last_reply(peer_uuid) - time.time())  < taco.constants.ROLLCALL_TIMEOUT:
        peers_i_can_talk_to.append(peer_uuid)
    response = {taco.constants.NET_REPLY:taco.constants.NET_REPLY_ROLLCALL,taco.constants.NET_DATABLOCK:[taco.globals.settings["Nickname"],taco.globals.settings["Local UUID"]] + peers_i_can_talk_to}
  return msgpack.packb(response)
 
def Process_Reply_Rollcall(peer_uuid,unpacked):
  requested_peers = []
  with taco.globals.settings_lock:
    new_nickname = unpacked[0]
    if taco.globals.settings["Peers"].has_key(peer_uuid):
      if taco.globals.settings["Peers"][peer_uuid].has_key("nickname"):
        if taco.globals.settings["Peers"][peer_uuid]["nickname"]!= new_nickname:
          if taco.constants.NICKNAME_CHECKER.match(new_nickname):
            taco.globals.settings["Peers"][peer_uuid]["nickname"] = new_nickname
      else:
        if taco.constants.NICKNAME_CHECKER.match(new_nickname):
          taco.globals.settings["Peers"][peer_uuid]["nickname"] = new_nickname
    for peerid in unpacked[1:]:
      if taco.constants.UUID_CHECKER.match(peerid):
        if peerid not in taco.globals.settings["Peers"].keys() and peerid != taco.globals.settings["Local UUID"]:
          requested_peers.append(peerid)
  if len(requested_peers) > 0:
    return Request_Certs(requested_peers)
  return ""
    
        
 
def Request_Certs(peer_uuids):
  request = {taco.constants.NET_REQUEST:taco.constants.NET_REQUEST_CERTS,taco.constants.NET_DATABLOCK:peer_uuids}
  return msgpack.packb(request)

def Reply_Certs(peer_uuids):
  response = {taco.constants.NET_REPLY:taco.constants.NET_REPLY_CERTS,taco.constants.NET_DATABLOCK:{}}
  with taco.globals.settings_lock:
    for peer_uuid in peer_uuids:
      if taco.globals.settings["Peers"].has_key(peer_uuid):
        response[taco.constants.NET_DATABLOCK][peer_uuid] = [taco.globals.settings["Peers"][peer_uuid]["hostname"],taco.globals.settings["Peers"][peer_uuid]["port"],taco.globals.settings["Peers"][peer_uuid]["clientkey"],taco.globals.settings["Peers"][peer_uuid]["serverkey"],taco.globals.settings["Peers"][peer_uuid]["dynamic"]]
  return msgpack.packb(response)

def Process_Reply_Certs(peer_uuid,unpacked):
  response = ""
  logging.debug("Got some new peers to add:" + str(unpacked))
  if type(unpacked) == type({}):
    for peerid in unpacked.keys():
      if len(unpacked[peerid]) == 5:
        (hostname,port,clientkey,serverkey,dynamic) = unpacked[peerid]
        with taco.globals.settings_lock:
          if not taco.globals.settings["Peers"].has_key(peerid):
            taco.globals.settings["Peers"][peerid] = {}
            taco.globals.settings["Peers"][peerid]["hostname"] = hostname
            taco.globals.settings["Peers"][peerid]["port"] = int(port)
            taco.globals.settings["Peers"][peerid]["clientkey"] = clientkey
            taco.globals.settings["Peers"][peerid]["serverkey"] = serverkey
            taco.globals.settings["Peers"][peerid]["dynamic"] = int(dynamic)
            taco.globals.settings["Peers"][peerid]["enabled"] = 0
            taco.globals.settings["Peers"][peerid]["localnick"] = ""
            taco.globals.settings["Peers"][peerid]["nickname"] = "Peer Nickname"
            taco.settings.Save_Settings(False)
      

  return response
  
