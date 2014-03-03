import os
import logging
import time
import threading
import Queue
import random
import taco.constants
import taco.globals
import uuid

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
  with taco.globals.settings_lock:
    for [sharename,sharepath] in taco.globals.settings["Shares"]:
      dirpath = os.path.abspath(os.path.normcase(unicode(sharepath)))
      dirpath2 = os.path.abspath(os.path.normcase(unicode(path)))
      if os.path.commonprefix([dirpath,dirpath2]) == dirpath:
        return_value = True
        break
  logging.debug(path + " -- " + str(return_value))
  return return_value

def Convert_Share_To_Path(share):
  return_val = ""
  with taco.globals.settings_lock:
    for [sharename,sharepath] in taco.globals.settings["Shares"]:
      if sharename==share:
        return_val = sharepath
        break
  logging.debug(share + " -- " + str(return_val))
  return return_val

class TacoFilesystemManager(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

    self.stop = False
    self.stop_lock = threading.Lock()

    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1

    self.workers = []
    self.last_purge = time.time()

    self.listings_lock = threading.Lock()
    self.listings = {}

    self.listing_work_queue = Queue.Queue()
    self.listing_results_queue = Queue.Queue()
  
    self.results_to_return = []

    self.download_q_check_time = time.time()
    self.client_downloading = {}
    self.client_downloading_status = {}
    self.client_downloading_chunk_uuid = {}
 
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

  def stop_running(self):
    with self.stop_lock:
      self.stop = True
      
  def continue_running(self):
    with self.stop_lock:
      continue_run = not self.stop
    return continue_run    
        
  def run(self):
    self.set_status("Starting Up Filesystem Manager")
    for i in range(taco.constants.FILESYSTEM_WORKER_COUNT):
      self.workers.append(TacoFilesystemWorker(i))
    for i in self.workers:
      i.start()
    self.did_something = True
    while self.continue_running():
      if not self.did_something: time.sleep(0.01 + random.uniform(0.01, 0.1))
      self.did_something = False
      if not self.continue_running(): break

      #DOWNLOAD Q CHECK
      if time.time() >= self.download_q_check_time:
        #self.set_status("Checking if the download q is in a good state")
        with taco.globals.settings_lock: local_copy_download_directory = os.path.normpath(taco.globals.settings["Download Location"])
        self.download_q_check_time = time.time() + taco.constants.DOWNLOAD_Q_CHECK_TIME
        with taco.globals.download_q_lock:
          for peer_uuid in taco.globals.download_q.keys():
            if len(taco.globals.download_q[peer_uuid]) > 0:
              (sharedir,filename,filesize,filemod) = taco.globals.download_q[peer_uuid][0]
              if not self.client_downloading.has_key(peer_uuid): self.client_downloading[peer_uuid] = 0
              if self.client_downloading[peer_uuid] != (sharedir,filename,filesize,filemod):
                self.set_status("File we should be downloading has changed:" + str((peer_uuid,sharedir,filename,filesize,filemod)))
                self.client_downloading[peer_uuid] = (sharedir,filename,filesize,filemod)
                self.did_something = True
            else:
              self.client_downloading[peer_uuid] = 0 #download q empty

        #send out requests for downloadq items
        for peer_uuid in self.client_downloading.keys():
          (sharedir,filename,filesize,filemod) = self.client_downloading[peer_uuid]
          if not self.client_downloading_status.has_key(peer_uuid): self.client_downloading_status[peer_uuid] = (0.0,0.0,0)
          (time_request_sent,time_request_ack,offset) = self.client_downloading_status[peer_uuid]
          if time_request_sent == 0.0: #request more data
            if os.path.isdir(local_copy_download_directory):
              filename_incomplete = os.path.normpath(local_copy_download_directory + u"/" + filename + taco.constants.FILESYSTEM_WORKINPROGRESS_SUFFIX)
              filename_complete = os.path.normpath(local_copy_download_directory + u"/" + filename)
              if os.path.isfile(filename_complete) and os.path.getsize(filename_complete) == filesize:
                pass #file download is complete, or has been re-requested on a filename of the same size do cleanup/ignore
              if os.path.isfile(filename_incomplete) and os.path.getsize(filename_incomplete) != filesize:
                pass #file is partially downloaded, download more

            #self.client_downloading_chunk_uuid[peer_uuid] = uuid.uuid4().hex
            #self.client_downloading_status[peer_uuid] = (time.time(),0.0,0)
          elif abs(time.time() - time_request_sent) > taco.constants.DOWNLOAD_Q_WAIT_FOR_ACK: #too much time has passed since we sent the request for data, and have gotten no ack,re-requesting
            self.client_downloading_status[peer_uuid] = (0.0,0.0,0)
          elif abs(time.time() - time_request_ack)  > taco.constants.DOWNLOAD_Q_WAIT_FOR_DATA: #too much time has passed since we got an ack for the data, and have gotten no data,re-requesting
            self.client_downloading_status[peer_uuid] = (0.0,0.0,0)

      if len(self.results_to_return) > 0:
        self.set_status("There are results that need to be sent once they are ready")
        with self.listings_lock:
          for [peer_uuid,sharedir,shareuuid] in self.results_to_return:
            if sharedir in self.listings.keys():
              self.set_status("RESULTS ready to send:" + str((sharedir,shareuuid))) 
              request = taco.commands.Request_Share_Listing_Results(sharedir,shareuuid,self.listings[sharedir])
              taco.globals.Add_To_Output_Queue(peer_uuid,request,2)
              self.results_to_return.remove([peer_uuid,sharedir,shareuuid])
              self.did_something = True
              
                 
      if abs(time.time() - self.last_purge) > taco.constants.FILESYSTEM_CACHE_PURGE:
        self.set_status("Purging old filesystem results")
        self.last_purge = time.time()

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
            self.did_something = True

      while not self.listing_results_queue.empty():
        (success,thetime,sharedir,dirs,files) = self.listing_results_queue.get()
        self.set_status("Processing a worker result: " + sharedir)
        self.add_listing(thetime,sharedir,dirs,files)
        self.did_something = True
      
      if not self.continue_running(): break
    self.set_status("Exiting")
    for i in self.workers:
      i.stop_running()
    for i in self.workers:
      i.join()

class TacoFilesystemWorker(threading.Thread):
  def __init__(self,worker_id):
    threading.Thread.__init__(self)

    self.stop = False
    self.stop_lock = threading.Lock()

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

  def stop_running(self):
    with self.stop_lock:
      self.stop = True

  def continue_running(self):
    with self.stop_lock:
      continue_run = not self.stop
    return continue_run
  
  def run(self):
    self.set_status("Starting Filesystem Worker #" + str(self.worker_id))
    self.did_something = True
    while self.continue_running():
      if not self.did_something: time.sleep(random.uniform(0.01, 0.1))
      self.did_something = False
      if not self.continue_running(): break
      try:
        rootsharedir = taco.globals.filesys.listing_work_queue.get(True,0.25)
        self.set_status(str(self.worker_id) + " -- " + str(rootsharedir))
        rootsharedir = os.path.normpath(rootsharedir)
        logging.debug("rootsharedir: " + rootsharedir + " -- " + os.path.normpath(rootsharedir))
        rootsharename = rootsharedir.split(u"/")[1]
        rootpath = os.path.normpath(u"/" + u"/".join(rootsharedir.split(u"/")[2:]) + u"/")
        logging.debug("rootsharename:" + rootsharename) 
        logging.debug("rootpath:" + rootpath) 
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
      self.did_something = True

    self.set_status("Exiting Filesystem Worker #" + str(self.worker_id))

