import taco.globals
import taco.constants
import taco.settings
import msgpack
import logging
import time
import uuid
import Queue

def Create_Request(command=taco.constants.NET_GARBAGE,data=""):
  with taco.globals.settings_lock: 
    localuuid = taco.globals.settings["Local UUID"]
  response = {taco.constants.NET_IDENT:localuuid,taco.constants.NET_REQUEST:command,taco.constants.NET_DATABLOCK:data}
  return response

def Create_Reply(command=taco.constants.NET_GARBAGE,data=""):
  with taco.globals.settings_lock: 
    localuuid = taco.globals.settings["Local UUID"]
  reply = {taco.constants.NET_IDENT:localuuid,taco.constants.NET_REPLY:command,taco.constants.NET_DATABLOCK:data}
  return reply

def Proccess_Request(packed):
  reply = Create_Request()
  try:
    unpacked = msgpack.unpackb(packed)
    assert taco.constants.NET_DATABLOCK in unpacked
    assert taco.constants.NET_IDENT in unpacked
  except:
    logging.warning("Got a bad request")
    return ("0",msgpack.packb(reply))
  if taco.constants.NET_REQUEST in unpacked:
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_GIVE_FILE_CHUNK:
      if "data" in unpacked[taco.constants.NET_DATABLOCK]:
        logging.info("NET_REQUEST (FileChunk DATA): " + str(len(unpacked[taco.constants.NET_DATABLOCK]["data"])))
    else:
      logging.info("NET_REQUEST: " + str(unpacked))
    IDENT = unpacked[taco.constants.NET_IDENT]
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_ROLLCALL:              return (IDENT,Reply_Rollcall())
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_CERTS:                 return (IDENT,Reply_Certs(IDENT,unpacked[taco.constants.NET_DATABLOCK]))
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_CHAT:                  return (IDENT,Reply_Chat(IDENT,unpacked[taco.constants.NET_DATABLOCK]))
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_SHARE_LISTING:         return (IDENT,Reply_Share_Listing(IDENT,unpacked[taco.constants.NET_DATABLOCK]))
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_SHARE_LISTING_RESULTS: return (IDENT,Reply_Share_Listing_Result(IDENT,unpacked[taco.constants.NET_DATABLOCK]))
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_GET_FILE_CHUNK:        return (IDENT,Reply_Get_File_Chunk(IDENT,unpacked[taco.constants.NET_DATABLOCK]))
    if unpacked[taco.constants.NET_REQUEST] == taco.constants.NET_REQUEST_GIVE_FILE_CHUNK:       return (IDENT,Reply_Give_File_Chunk(IDENT,unpacked[taco.constants.NET_DATABLOCK]))

  logging.debug("Unknown Request") 
  return ("0",msgpack.packb(reply))

def Process_Reply(peer_uuid,packed):
  response = ""
  try:
    unpacked = msgpack.unpackb(packed)
    assert taco.constants.NET_DATABLOCK in unpacked
    assert taco.constants.NET_IDENT in unpacked
  except:
    logging.debug("Bad Reply")
    return response
  if taco.constants.NET_REPLY in unpacked:
    logging.info("NET_REPLY: " + str(unpacked))
    if unpacked[taco.constants.NET_REPLY] == taco.constants.NET_REPLY_ROLLCALL:       return Process_Reply_Rollcall(peer_uuid,unpacked[taco.constants.NET_DATABLOCK])
    if unpacked[taco.constants.NET_REPLY] == taco.constants.NET_REPLY_CERTS:          return Process_Reply_Certs(peer_uuid,unpacked[taco.constants.NET_DATABLOCK])
    if unpacked[taco.constants.NET_REPLY] == taco.constants.NET_REPLY_GET_FILE_CHUNK: return Process_Reply_Get_File_Chunk(peer_uuid,unpacked[taco.constants.NET_DATABLOCK])

  return response

def Request_Chat(chatmsg):
  output_block = Create_Request(taco.constants.NET_REQUEST_CHAT,[time.time(),chatmsg])
  with taco.globals.chat_log_lock:
    taco.globals.chat_log.append([taco.globals.settings["Local UUID"],time.time(),chatmsg])
    with taco.globals.chat_uuid_lock:
      taco.globals.chat_uuid = uuid.uuid4().hex
    if len(taco.globals.chat_log) > taco.constants.CHAT_LOG_MAXSIZE:
      taco.globals.chat_log = taco.globals.chat_log[1:]

  taco.globals.Add_To_All_Output_Queues(msgpack.packb(output_block))

def Reply_Chat(peer_uuid,datablock):
  logging.debug(str(datablock))
  with taco.globals.chat_log_lock:
    taco.globals.chat_log.append([peer_uuid] + datablock)
    with taco.globals.chat_uuid_lock:
      taco.globals.chat_uuid = uuid.uuid4().hex
    if len(taco.globals.chat_log) > taco.constants.CHAT_LOG_MAXSIZE:
      taco.globals.chat_log = taco.globals.chat_log[1:]
  reply = Create_Reply(taco.constants.NET_REPLY_CHAT,{})
  return msgpack.packb(reply)

def Request_Rollcall():
  request = Create_Request(taco.constants.NET_REQUEST_ROLLCALL,"")
  return msgpack.packb(request)

def Reply_Rollcall():
  peers_i_can_talk_to = []
  with taco.globals.settings_lock:
    for peer_uuid in taco.globals.settings["Peers"].keys():
      if abs(taco.globals.clients.get_client_last_reply(peer_uuid) - time.time())  < taco.constants.ROLLCALL_TIMEOUT:
        peers_i_can_talk_to.append(peer_uuid)
  reply = Create_Reply(taco.constants.NET_REPLY_ROLLCALL,[taco.globals.settings["Nickname"],taco.globals.settings["Local UUID"]] + peers_i_can_talk_to)
  return msgpack.packb(reply)
 
def Process_Reply_Rollcall(peer_uuid,unpacked):
  requested_peers = []
  #logging.warning(str(unpacked))
  with taco.globals.settings_lock:
    new_nickname = unpacked[0]
    if peer_uuid in taco.globals.settings["Peers"]:
      if "nickname" in taco.globals.settings["Peers"][peer_uuid]:
        if taco.globals.settings["Peers"][peer_uuid]["nickname"]!= new_nickname:
          if taco.constants.NICKNAME_CHECKER.match(new_nickname):
            taco.globals.settings["Peers"][peer_uuid]["nickname"] = new_nickname
            taco.settings.Save_Settings(False)
      else:
        if taco.constants.NICKNAME_CHECKER.match(new_nickname):
          taco.globals.settings["Peers"][peer_uuid]["nickname"] = new_nickname
          taco.settings.Save_Settings(False)
    for peerid in unpacked[1:]:
      if taco.constants.UUID_CHECKER.match(peerid):
        if peerid not in taco.globals.settings["Peers"].keys() and peerid != taco.globals.settings["Local UUID"]:
          requested_peers.append(peerid)
  if len(requested_peers) > 0:
    return Request_Certs(requested_peers)
  return ""
    
        
 
def Request_Certs(peer_uuids):
  request =  Create_Request(taco.constants.NET_REQUEST_CERTS,peer_uuids)
  return msgpack.packb(request)

def Reply_Certs(peer_uuid,datablock):
  reply = Create_Reply(taco.constants.NET_REPLY_CERTS,{})
  with taco.globals.settings_lock:
    for peer_uuid in datablock:
      if peer_uuid in taco.globals.settings["Peers"]:
        reply[taco.constants.NET_DATABLOCK][peer_uuid] = [taco.globals.settings["Peers"][peer_uuid]["nickname"],taco.globals.settings["Peers"][peer_uuid]["hostname"],taco.globals.settings["Peers"][peer_uuid]["port"],taco.globals.settings["Peers"][peer_uuid]["clientkey"],taco.globals.settings["Peers"][peer_uuid]["serverkey"],taco.globals.settings["Peers"][peer_uuid]["dynamic"]]
  return msgpack.packb(reply)

def Process_Reply_Certs(peer_uuid,unpacked):
  response = ""
  logging.debug("Got some new peers to add:" + str(unpacked))
  if type(unpacked) == type({}):
    for peerid in unpacked.keys():
      if len(unpacked[peerid]) == 6:
        (nickname,hostname,port,clientkey,serverkey,dynamic) = unpacked[peerid]
        with taco.globals.settings_lock:
          if not peerid in taco.globals.settings["Peers"]:
            taco.globals.settings["Peers"][peerid] = {}
            taco.globals.settings["Peers"][peerid]["hostname"] = hostname
            taco.globals.settings["Peers"][peerid]["port"] = int(port)
            taco.globals.settings["Peers"][peerid]["clientkey"] = clientkey
            taco.globals.settings["Peers"][peerid]["serverkey"] = serverkey
            taco.globals.settings["Peers"][peerid]["dynamic"] = int(dynamic)
            taco.globals.settings["Peers"][peerid]["enabled"] = 0
            taco.globals.settings["Peers"][peerid]["localnick"] = ""
            taco.globals.settings["Peers"][peerid]["nickname"] = nickname
            taco.settings.Save_Settings(False)
      

  return response
 

def Request_Share_Listing(peer_uuid,sharedir,share_listing_uuid):
  with taco.globals.share_listings_i_care_about_lock:
    taco.globals.share_listings_i_care_about[share_listing_uuid] = time.time()
  request =  Create_Request(taco.constants.NET_REQUEST_SHARE_LISTING,{"sharedir":sharedir,"results_uuid":share_listing_uuid})
  return msgpack.packb(request)

def Reply_Share_Listing(peer_uuid,datablock):
  reply = Create_Reply(taco.constants.NET_REPLY_SHARE_LISTING,1)
  try:
    sharedir = datablock["sharedir"]
    shareuuid = datablock["results_uuid"]
  except:
    reply[taco.constants.NET_DATABLOCK] = 0
    return msgpack.packb(reply)

  #logging.debug("Got a share listing request from: " + peer_uuid + " for: " + sharedir)
  with taco.globals.share_listing_requests_lock:
    if not peer_uuid in taco.globals.share_listing_requests: taco.globals.share_listing_requests[peer_uuid] = Queue.Queue()
    taco.globals.share_listing_requests[peer_uuid].put((sharedir,shareuuid))
    taco.globals.filesys.sleep.set()

  return msgpack.packb(reply)

def Request_Share_Listing_Results(sharedir,results_uuid,results):
  request =  Create_Request(taco.constants.NET_REQUEST_SHARE_LISTING_RESULTS,{"sharedir":sharedir,"results_uuid":results_uuid,"results":results}) 
  return msgpack.packb(request)

def Reply_Share_Listing_Result(peer_uuid,datablock):
  reply = Create_Reply(taco.constants.NET_REPLY_SHARE_LISTING_RESULTS,1)
  try:
    sharedir = datablock["sharedir"]
    shareuuid = datablock["results_uuid"]
    results   = datablock["results"]
    with taco.globals.share_listings_i_care_about_lock:
      assert shareuuid in taco.globals.share_listings_i_care_about
  except:
    reply = Create_Reply(taco.constants.NET_REPLY_SHARE_LISTING_RESULTS,0)
    return msgpack.packb(reply)
  
  #logging.debug("Got share listing RESULTS from: " + peer_uuid + " for: " + sharedir)
  with taco.globals.share_listings_lock:
    taco.globals.share_listings[(peer_uuid,sharedir)] = [time.time(),results]
  with taco.globals.share_listings_i_care_about_lock:
    del taco.globals.share_listings_i_care_about[shareuuid]

  return msgpack.packb(reply)

def Request_Get_File_Chunk(sharedir,filename,offset,chunk_uuid):
  request = Create_Request(taco.constants.NET_REQUEST_GET_FILE_CHUNK,{"sharedir":sharedir,"filename":filename,"offset":offset,"chunk_uuid":chunk_uuid})
  return msgpack.packb(request)

def Reply_Get_File_Chunk(peer_uuid,datablock):
  try:
    sharedir   = datablock["sharedir"]
    filename   = datablock["filename"]
    offset     = int(datablock["offset"])
    chunk_uuid = datablock["chunk_uuid"]
  except:
    reply = Create_Reply(taco.constants.NET_REPLY_GET_FILE_CHUNK,{"status":0})
    return msgpack.packb(reply)
  taco.globals.filesys.chunk_requests_outgoing_queue.put((peer_uuid,sharedir,filename,offset,chunk_uuid))
  taco.globals.filesys.sleep.set()
  reply = Create_Reply(taco.constants.NET_REPLY_GET_FILE_CHUNK,{"chunk_uuid":chunk_uuid,"status":1})
  return msgpack.packb(reply)

def Process_Reply_Get_File_Chunk(peer_uuid,datablock):
  try:
    status     = datablock["status"]
    chunk_uuid = datablock["chunk_uuid"] 
  except:
    return ""
  taco.globals.filesys.chunk_requests_ack_queue.put((peer_uuid,chunk_uuid))
  taco.globals.filesys.sleep.set()
  return ""
    
def Request_Give_File_Chunk(data,chunk_uuid):
  request = Create_Request(taco.constants.NET_REQUEST_GIVE_FILE_CHUNK,{"data":data,"chunk_uuid":chunk_uuid})
  return msgpack.packb(request)

def Reply_Give_File_Chunk(peer_uuid,datablock):
  reply = Create_Reply()
  try:
    chunk_uuid = datablock["chunk_uuid"]
    data = datablock["data"]
  except:
    return msgpack.packb(reply)
  taco.globals.filesys.chunk_requests_incoming_queue.put((peer_uuid,chunk_uuid,data))
  taco.globals.filesys.sleep.set()
  return msgpack.packb(reply)
