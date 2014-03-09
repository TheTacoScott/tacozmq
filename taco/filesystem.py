import os
import logging
import time
import threading
import Queue
import random
import taco.constants
import taco.globals
import uuid
from collections import defaultdict

if os.name=='nt':
  import ctypes
  def Get_Free_Space(path):
    free_bytes = ctypes.c_ulonglong(0)
    total = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(path), None, ctypes.pointer(total), ctypes.pointer(free_bytes))
    return (free_bytes.value,total.value)

elif os.name=='posix':
  def Get_Free_Space(path):
    try:
      data  = os.statvfs(path)
      free  = data.f_bavail * data.f_frsize
      total = data.f_blocks * data.f_frsize
      return (free,total)
    except:
      return (0,0)

def Is_Path_Under_A_Share(path):
  return_value = False
  if os.path.isdir(os.path.normpath(path)):
    with taco.globals.settings_lock:
      for [sharename,sharepath] in taco.globals.settings["Shares"]:
        dirpath = os.path.abspath(os.path.normcase(unicode(sharepath)))
        dirpath2 = os.path.abspath(os.path.normcase(unicode(path)))
        if os.path.commonprefix([dirpath,dirpath2]) == dirpath:
          return_value = True
          break
  #logging.debug(path + " -- " + str(return_value))
  return return_value

def Convert_Share_To_Path(share):
  return_val = ""
  with taco.globals.settings_lock:
    for [sharename,sharepath] in taco.globals.settings["Shares"]:
      if sharename==share:
        return_val = sharepath
        break
  #logging.debug(share + " -- " + str(return_val))
  return return_val

class TacoFilesystemManager(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop = threading.Event()
    self.sleep = threading.Event()

    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1

    self.workers = []
    self.last_purge = time.time()

    self.listings_lock = threading.Lock()
    self.listings = {}

    self.listing_work_queue            = Queue.Queue()
    self.listing_results_queue         = Queue.Queue()
    self.chunk_requests_incoming_queue = Queue.Queue() 
    self.chunk_requests_outgoing_queue = Queue.Queue() 
    self.chunk_requests_ack_queue      = Queue.Queue() 

    self.results_to_return = []

    self.download_q_check_time = time.time()
    self.client_downloading = {}
    self.client_downloading_status = defaultdict(dict)
    self.client_downloading_pending_chunks = {}
    self.client_downloading_requested_chunks = {}
    self.client_downloading_filename = {} 
    self.files_w = {}
    self.files_r = {}
    self.files_r_last_access = {}
    self.files_w_last_access = {}
 
  def add_listing(self,thetime,sharedir,dirs,files):
    with self.listings_lock:
      self.listings[sharedir] = [thetime,dirs,files]

  def set_status(self,text,level=0):
    if   level==1: logging.info(text)
    elif level==0: logging.debug(text)
    elif level==2: logging.warning(text)
    elif level==3: logging.error(text)
    with self.status_lock:
      self.status = text
      self.status_time = time.time()

  def get_status(self):
    with self.status_lock:
      return (self.status,self.status_time)

  def run(self):
    self.set_status("Starting Up Filesystem Manager")
    for i in range(taco.constants.FILESYSTEM_WORKER_COUNT):
      self.workers.append(TacoFilesystemWorker(i))
    for i in self.workers:
      i.start()
    while not self.stop.is_set():
      #self.set_status("FILESYS")
      self.sleep.wait(0.2)
      self.sleep.clear()
      if self.stop.is_set(): break
      
      #CHECK downloadq state
      if time.time() >= self.download_q_check_time:
        #self.set_status("Checking if the download q is in a good state")
        with taco.globals.settings_lock: local_copy_download_directory = os.path.normpath(taco.globals.settings["Download Location"])
        self.download_q_check_time = time.time() + taco.constants.DOWNLOAD_Q_CHECK_TIME

        #check for download q items
        with taco.globals.download_q_lock:
          for peer_uuid in taco.globals.download_q.keys():
            if len(taco.globals.download_q[peer_uuid]) == 0:
              self.set_status("Download Q empty for: " + peer_uuid)
              self.client_downloading[peer_uuid] = 0
              del taco.globals.download_q[peer_uuid]
              continue
            else:
              (sharedir,filename,filesize,filemod) = taco.globals.download_q[peer_uuid][0]
              if not peer_uuid in self.client_downloading: self.client_downloading[peer_uuid] = 0

              if self.client_downloading[peer_uuid] != (sharedir,filename,filesize,filemod):
                self.set_status("Need to check on the file we should be downloading:" + str((peer_uuid,sharedir,filename,filesize,filemod)))
                self.client_downloading[peer_uuid] = (sharedir,filename,filesize,filemod)
                self.client_downloading_pending_chunks[peer_uuid] = []
                self.client_downloading_requested_chunks[peer_uuid] = []
                if not os.path.isdir(local_copy_download_directory): continue
                filename_incomplete = os.path.normpath(local_copy_download_directory + u"/" + filename + taco.constants.FILESYSTEM_WORKINPROGRESS_SUFFIX)

                try:
                  current_size = os.path.getsize(filename_incomplete)
                except:
                  current_size = 0
                if current_size != filesize:
                  self.set_status("Building in memory 'torrent'")
                  self.client_downloading_filename[peer_uuid] = filename_incomplete
                  self.client_downloading_status = defaultdict(dict)
                  for file_offset in range(current_size,filesize+1,taco.constants.FILESYSTEM_CHUNK_SIZE):
                    tmp_uuid = uuid.uuid4().hex
                    self.client_downloading_pending_chunks[peer_uuid].append((tmp_uuid,file_offset))
                    self.client_downloading_status[peer_uuid][tmp_uuid] = (0.0,0.0,file_offset)
                  self.client_downloading_pending_chunks[peer_uuid].reverse()
                  self.set_status("Building in memory 'torrent' -- done")
              else:
                if not os.path.isdir(local_copy_download_directory): continue
                filename_incomplete = os.path.normpath(local_copy_download_directory + u"/" + filename + taco.constants.FILESYSTEM_WORKINPROGRESS_SUFFIX)
                filename_complete   = os.path.normpath(local_copy_download_directory + u"/" + filename)
                try:
                  current_size = os.path.getsize(filename_incomplete)
                except:
                  current_size = 0
                #self.set_status(str((current_size,filesize,len(self.client_downloading_pending_chunks[peer_uuid]),len(self.client_downloading_requested_chunks[peer_uuid]))))
                if current_size == filesize and len(self.client_downloading_pending_chunks[peer_uuid]) == 0 and len(self.client_downloading_requested_chunks[peer_uuid]) == 0:
                  self.set_status("FILE DOWNLOAD COMPLETE")
                  if not os.path.exists(filename_complete):
                    os.rename(filename_incomplete,filename_complete)
                  else:
                    (root,ext) = os.path.splitext(filename_complete)
                    filename_complete = root + u"." + unicode(uuid.uuid4().hex) + u"." + ext
                    os.rename(filename_incomplete,filename_complete)
                  with taco.globals.completed_q_lock:
                    taco.globals.completed_q.append((time.time(),peer_uuid,sharedir,filename,filesize))
                  del taco.globals.download_q[peer_uuid][0]


      #send out requests for downloads 
      for peer_uuid in self.client_downloading:
        if self.client_downloading[peer_uuid] == 0: continue
        (sharedir,filename,filesize,filemod) = self.client_downloading[peer_uuid]
        while len(self.client_downloading_pending_chunks[peer_uuid]) > 0 and len(self.client_downloading_requested_chunks[peer_uuid]) < taco.constants.FILESYSTEM_CREDIT_MAX: 
          (chunk_uuid,file_offset) = self.client_downloading_pending_chunks[peer_uuid].pop()
          self.set_status("Credits Free:" + str((sharedir,filename,filesize,filemod,chunk_uuid,file_offset)))
          request = taco.commands.Request_Get_File_Chunk(sharedir,filename,file_offset,chunk_uuid)
          taco.globals.Add_To_Output_Queue(peer_uuid,request,4)
          self.client_downloading_requested_chunks[peer_uuid].append(chunk_uuid)
          (time_request_sent,time_request_ack,offset) = self.client_downloading_status[peer_uuid][chunk_uuid]
          self.client_downloading_status[peer_uuid][chunk_uuid] = (time.time(),0.0,offset)
      
      #check for chunk ack
      while not self.chunk_requests_ack_queue.empty():
        try:
          (peer_uuid,chunk_uuid) = self.chunk_requests_ack_queue.get(0)
        except:
          break
        if peer_uuid in self.client_downloading_requested_chunks and chunk_uuid in self.client_downloading_requested_chunks[peer_uuid] and peer_uuid in self.client_downloading_status:
          (time_request_sent,time_request_ack,offset) = self.client_downloading_status[peer_uuid][chunk_uuid]
          self.client_downloading_status[peer_uuid][chunk_uuid] = (time_request_sent,time.time(),offset)
          self.set_status("File Chunk request has been ACK'D:" + str((peer_uuid,time_request_sent,chunk_uuid)))
          self.sleep.set()

      #if chunk has not been ack'd in > x time or no data in > x time
      for peer_uuid in self.client_downloading_status:
        for chunk_uuid in self.client_downloading_status[peer_uuid]:
          (time_request_sent,time_request_ack,offset) = self.client_downloading_status[peer_uuid][chunk_uuid]
          if time_request_sent > 0.0 and peer_uuid in self.client_downloading:
            if time_request_ack == 0.0:
              if abs(time.time() - time_request_sent) > taco.constants.DOWNLOAD_Q_WAIT_FOR_ACK:
                self.set_status("Download is hosed up (no ack) for: " + peer_uuid)
                self.client_downloading[peer_uuid] = 0
                break
            elif time_request_ack > 0.0:
              if abs(time.time() - time_request_ack) > taco.constants.DOWNLOAD_Q_WAIT_FOR_DATA:
                self.set_status("Download is hosed up (no data for too long) for: " + peer_uuid)
                self.client_downloading[peer_uuid] = 0
                break

      #chunk data has been recieved
      while not self.chunk_requests_incoming_queue.empty():
        if self.stop.is_set(): break
        try:
          (peer_uuid,chunk_uuid,data) = self.chunk_requests_incoming_queue.get(0)
        except:
          break
        if peer_uuid in self.client_downloading_requested_chunks and chunk_uuid in self.client_downloading_requested_chunks[peer_uuid] and peer_uuid in self.client_downloading_filename:
          if peer_uuid in self.client_downloading and self.client_downloading[peer_uuid] == 0: continue
          self.set_status("Chunk data has been recieved: " + str((peer_uuid,chunk_uuid,len(data))))
          (sharedir,filename,filesize,filemod) = self.client_downloading[peer_uuid]
          fullpath = self.client_downloading_filename[peer_uuid]
          if fullpath not in self.files_w.keys():
            self.files_w[fullpath] = open(fullpath,"ab")
          self.files_w_last_access[fullpath] = time.time()
          self.files_w[fullpath].write(data)
          self.files_w[fullpath].flush()
          if self.files_w[fullpath].tell() >= filesize:
            self.files_w[fullpath].close()
            del self.files_w[fullpath]
          del self.client_downloading_status[peer_uuid][chunk_uuid]
          self.client_downloading_requested_chunks[peer_uuid].remove(chunk_uuid)
          self.sleep.set()
        else:
          self.set_status("Got a chunk, but it's bogus:" + str((peer_uuid,chunk_uuid,len(data))))

      if self.stop.is_set(): break

      #chunk data has been requested 
      if not self.chunk_requests_outgoing_queue.empty():
        if self.stop.is_set(): break
        try:
          (peer_uuid,sharedir,filename,offset,chunk_uuid) = self.chunk_requests_outgoing_queue.get(0)
        except:
          break
        self.set_status("Need to send a chunk of data: " + str((peer_uuid,sharedir,filename,offset,chunk_uuid)))
        rootsharename = sharedir.split(u"/")[1]
        rootpath = os.path.normpath(u"/" + u"/".join(sharedir.split(u"/")[2:]) + u"/")
        directory = os.path.normpath(Convert_Share_To_Path(rootsharename) + u"/" + rootpath)
        fullpath = os.path.normpath(directory + u"/" + filename)
        if not Is_Path_Under_A_Share(os.path.dirname(fullpath)): break
        if not os.path.isdir(directory): break
        if fullpath not in self.files_r.keys():
          self.set_status("I need to open a file for reading:" + fullpath)
          self.files_r[fullpath] = open(fullpath,"rb")
        self.files_r_last_access[fullpath] = time.time()
        if offset < os.path.getsize(fullpath):
          self.files_r[fullpath].seek(offset)
          chunk_data = self.files_r[fullpath].read(taco.constants.FILESYSTEM_CHUNK_SIZE)
          request = taco.commands.Request_Give_File_Chunk(chunk_data,chunk_uuid)
          taco.globals.Add_To_Output_Queue(peer_uuid,request,3)
          self.sleep.set()
          taco.globals.clients.sleep.set()

      if self.stop.is_set(): break
            
      if len(self.results_to_return) > 0:
        #self.set_status("There are results that need to be sent once they are ready")
        with self.listings_lock:
          for [peer_uuid,sharedir,shareuuid] in self.results_to_return:
            if sharedir in self.listings.keys():
              self.set_status("RESULTS ready to send:" + str((sharedir,shareuuid))) 
              request = taco.commands.Request_Share_Listing_Results(sharedir,shareuuid,self.listings[sharedir])
              taco.globals.Add_To_Output_Queue(peer_uuid,request,2)
              taco.globals.clients.sleep.set()
              self.results_to_return.remove([peer_uuid,sharedir,shareuuid])
              self.sleep.set()
              
                 
      if abs(time.time() - self.last_purge) > taco.constants.FILESYSTEM_CACHE_PURGE:
        self.set_status("Purging old filesystem results")
        self.last_purge = time.time()
        
        for filename in self.files_r_last_access.keys():
          if abs(time.time() - self.files_r_last_access[filename]) > taco.constants.FILESYSTEM_CACHE_TIMEOUT:
            if filename in self.files_r.keys():
              self.set_status("Closing a file for reading due to inactivity:" + filename)
              self.files_r[filename].close()
              del self.files_r[filename]
            del self.files_r_last_access[filename]

        for filename in self.files_w_last_access.keys():
          if abs(time.time() - self.files_w_last_access[filename]) > taco.constants.FILESYSTEM_CACHE_TIMEOUT:
            if filename in self.files_w.keys():
              self.set_status("Closing a file for writing due to inactivity:" + filename)       
              self.files_w[filename].close()
              del self.files_w[filename]
            del self.files_w_last_access[filename]

        with taco.globals.share_listings_lock:
          for iterkey in taco.globals.share_listings.keys():
            if abs(time.time() - taco.globals.share_listings[iterkey][0]) > taco.constants.FILESYSTEM_CACHE_TIMEOUT:
              self.set_status("Purging old local filesystem cached results")
              del taco.globals.share_listings[iterkey]

        with self.listings_lock:
          for sharedir in self.listings.keys():
            [thetime,dirs,files] = self.listings[sharedir]
            if abs(time.time() - thetime) > taco.constants.FILESYSTEM_CACHE_TIMEOUT:
              self.set_status("Purging Filesystem cache for share: " + sharedir)
              del self.listings[sharedir]

        with taco.globals.share_listings_i_care_about_lock:
          for share_listing_uuid in taco.globals.share_listings_i_care_about.keys():
            thetime = taco.globals.share_listings_i_care_about[share_listing_uuid]
            if abs(time.time() - thetime) > taco.constants.FILESYSTEM_LISTING_TIMEOUT:
              self.set_status("Purging Filesystem listing i care about for: " + share_listing_uuid)
              del taco.globals.share_listings_i_care_about[share_listing_uuid]

      with taco.globals.share_listing_requests_lock:
        for peer_uuid in taco.globals.share_listing_requests.keys():
          while not taco.globals.share_listing_requests[peer_uuid].empty():
            (sharedir,shareuuid) = taco.globals.share_listing_requests[peer_uuid].get()
            self.set_status("Filesystem thread has a pending share listing request: " + str((sharedir,shareuuid)))
            rootsharedir = os.path.normpath(sharedir)
            rootsharename = rootsharedir.split(u"/")[1]
            rootpath = os.path.normpath(u"/" + u"/".join(rootsharedir.split(u"/")[2:]) + u"/")
            directory = os.path.normpath(Convert_Share_To_Path(rootsharename) + u"/" + rootpath)
            if (Is_Path_Under_A_Share(directory) and os.path.isdir(directory)) or rootsharedir == u"/":
              self.listing_work_queue.put(sharedir)
              self.results_to_return.append([peer_uuid,sharedir,shareuuid])
            else:
              self.set_status("User has requested a bogus share: " +str(sharedir))

      while not self.listing_results_queue.empty():
        (success,thetime,sharedir,dirs,files) = self.listing_results_queue.get()
        self.set_status("Processing a worker result: " + sharedir)
        self.add_listing(thetime,sharedir,dirs,files)
        self.sleep.set()
      
    self.set_status("Killing Workers")
    for i in self.workers:
      i.stop.set()
    for i in self.workers:
      i.join()
    self.set_status("Closing Open Files")
    for filename in self.files_r: self.files_r[filename].close()
    for filename in self.files_w: self.files_w[filename].close()
    self.set_status("Filesystem Manager Exit")


class TacoFilesystemWorker(threading.Thread):
  def __init__(self,worker_id):
    threading.Thread.__init__(self)

    self.stop = threading.Event()

    self.worker_id = worker_id

    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1

  def set_status(self,text,level=0):
    if   level==1: logging.info(text)
    elif level==0: logging.debug(text)
    elif level==2: logging.warning(text)
    elif level==3: logging.error(text)
    with self.status_lock:
      self.status = text
      self.status_time = time.time()

  def get_status(self):
    with self.status_lock:
      return (self.status,self.status_time)

  def run(self):
    self.set_status("Starting Filesystem Worker #" + str(self.worker_id))
    while not self.stop.is_set():
      try:
        rootsharedir = taco.globals.filesys.listing_work_queue.get(True,0.2)
        self.set_status(str(self.worker_id) + " -- " + str(rootsharedir))
        rootsharedir = os.path.normpath(rootsharedir)
        rootsharename = rootsharedir.split(u"/")[1]
        rootpath = os.path.normpath(u"/" + u"/".join(rootsharedir.split(u"/")[2:]) + u"/")
        directory = os.path.normpath(Convert_Share_To_Path(rootsharename) + u"/" + rootpath)
        if rootsharedir == u"/":
          self.set_status("Root share listing request")
          share_listing = []
          with taco.globals.settings_lock:
            for [sharename,sharepath] in taco.globals.settings["Shares"]:
              share_listing.append(sharename)
          share_listing.sort()
          results = [1,time.time(),rootsharedir,share_listing,[]]
          taco.globals.filesys.listing_results_queue.put(results)
          continue  
        assert Is_Path_Under_A_Share(directory)
        assert os.path.isdir(directory)
      except:
        continue
      self.set_status("Filesystem Worker #" + str(self.worker_id) + " -- Get Directory Listing for: " + directory)

      dirs = []
      files = []
      try:
        dirlist = os.listdir(directory)
      except:
        results = [0,time.time(),rootsharedir,[],[]]

      try:
        for fileobject in dirlist:
          joined = os.path.normpath(directory + u"/" + fileobject)
          if os.path.isfile(joined):
            filemod = os.stat(joined).st_mtime
            filesize = os.path.getsize(joined)
            files.append((fileobject,filesize,filemod))
          elif os.path.isdir(joined):
            dirs.append(fileobject)
        dirs.sort()
        files.sort()
        results = [1,time.time(),rootsharedir,dirs,files]
      except Exception,e:
        print str(e)
        results = [0,time.time(),rootsharedir,[],[]]

      taco.globals.filesys.listing_results_queue.put(results)
      taco.globals.filesys.sleep.set()

    self.set_status("Exiting Filesystem Worker #" + str(self.worker_id))

