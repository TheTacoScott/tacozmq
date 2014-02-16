import os
import logging
import time
import threading
import Queue
import taco.constants
import taco.globals

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
  return return_value

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

    self.files_open_for_w_lock = threading.Lock()
    self.files_open_for_w = {}
    self.files_open_for_w_time = {}

    self.files_open_for_r_lock = threading.Lock()
    self.files_open_for_r = {}
    self.files_open_for_r_time = {}

    self.listing_work_queue = Queue.Queue()
    self.results_queue = Queue.Queue()
 
  def add_listing(self,thetime,directory,dirs,files):
    with self.listings_lock:
      self.listings[directory] = [thetime,dirs,files]

  def set_status(self,text,level=0):
    if   level==1: logging.info(text)
    elif level==0: logging.debug(text)
    elif level==2: logging.warning(text)
    elif level==3: logging.error(text)
    with self.status_lock:
      self.status = text
      self.status_time = time.time()

  def get_directory_listing(self,directory):
    self.listing_work_queue.put(unicode(directory))

  def close_file_w(self,filename):
    self.set_status("Closing File for writing: " + filename)
    with self.files_open_for_w_lock:
      if filename in self.files_open_for_w.keys():
        self.files_open_for_w[filename].close()
        del self.files_open_for_w_time[filename]

  def close_file_r(self,filename):
    self.set_status("Closing File for reading: " + filename)
    with self.files_open_for_r_lock:
      if filename in self.files_open_for_r.keys():
        self.files_open_for_r[filename].close()
        del self.files_open_for_r_time[filename]
 
  def append_to_file(self,filename,data):
    if os.path.isfile(os.path.normpath(filename)):
      with self.files_open_for_w_lock:
        if filename not in self.files_open_for_w.keys():
          self.files_open_for_r[filename] = open(os.path.normpath(local_filename),"ab")
        self.files_open_for_r[filename].write(data)
        self.files_open_for_w_time[filename] = time.time()

  def read_from_file(self,filename,offset=0):
    if os.path.isfile(os.path.normpath(filename)):
      with self.files_open_for_r_lock:
        if filename not in self.files_open_for_r.keys():
          self.files_open_for_r[filename] = open(os.path.normpath(local_filename),"rb")
        self.files_open_for_r[filename].seek(offset)
        self.files_open_for_r_time[filename] = time.time()
        return self.files_open_for_r[filename].read(taco.constants.FILESYSTEM_CHUNK_SIZE)

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

    while self.continue_running():
      time.sleep(0.01)

      if not self.continue_running(): break
      
      if abs(time.time() - self.last_purge) > taco.constants.FILESYSTEM_CACHE_PURGE:
        self.set_status("Purging old filesystem results")
        self.last_purge = time.time()
        with self.listings_lock:
          for directory in self.listings.keys():
            [thetime,dirs,files] = self.listings[directory]
            if abs(time.time() - thetime) > taco.constants.FILESYSTEM_CACHE_TIMEOUT:
              self.set_status("Purging Filesystem cache for directory: " + directory)
              del self.listings[directory]

      with taco.globals.share_listing_requests_lock:
        for peer_uuid in taco.globals.share_listing_requests.keys():
          while not taco.globals.share_listing_requests[peer_uuid].empty():
            (sharename,sharepath,shareuuid) = taco.globals.share_listing_requests[peer_uuid].get()

      with self.files_open_for_r_lock:
        files_to_close = []
        for filename in self.files_open_for_r.keys():
          if abs(time.time() - self.files_open_for_r_time[filename] > taco.constants.FILESYSTEM_CACHE_PURGE):
            files_to_close.append(filename)
      for filename in files_to_close:
        self.close_file_r(filename)

      with self.files_open_for_w_lock:
        files_to_close = []
        for filename in self.files_open_for_w.keys():
          if abs(time.time() - self.files_open_for_w_time[filename] > taco.constants.FILESYSTEM_CACHE_PURGE):
            files_to_close.append(filename)
      for filename in files_to_close:
        self.close_file_w(filename)

      while not self.results_queue.empty():
        (success,thetime,directory,dirs,files) = self.results_queue.get()
        self.add_listing(thetime,directory,dirs,files)
      
      if not self.continue_running(): break
    self.set_status("Exiting")
    for i in self.workers:
      i.stop_running()
    for i in self.workers:
      i.join()
    files_to_close = []
    with self.files_open_for_r_lock:
      for filename in self.files_open_for_r.keys(): files_to_close.append(filename)
    for filename in files_to_close: self.close_file_r(filename)
    with self.files_open_for_w_lock:
      for filename in self.files_open_for_w.keys(): files_to_close.append(filename)
    for filename in files_to_close: self.close_file_w(filename)


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
    while self.continue_running():
      if not self.continue_running(): break
      try:
        directory = taco.globals.filesys.listing_work_queue.get(1,0.1)
      except:
        continue
      self.set_status("Filesystem Worker #" + str(self.worker_id) + " -- Get Directory Listing for: " + directory)

      dirs = []
      files = []
      try:
        dirlist = os.listdir(directory)
      except:
        results = [0,time.time(),directory,[],[]]

      try:
        for fileobject in dirlist:
          joined = os.path.normpath(os.path.join(ps.path.normpath(directory),fileobject))
          if os.path.isfile(joined):
            filemod = os.stat(joined).st_mtime
            filesize = os.path.getsize(joined)
            files.append(fileobject,filesize,filemod)
          elif os.path.isdir(joined):
            dirs.append(fileobject)
        dirs.sort()
        files.sort()
        results = [1,time.time(),directory,dirs,files]
      except:
        results = [0,time.time(),directory,[],[]]

      taco.globals.filesys.results_queue.put(results)

    self.set_status("Exiting Filesystem Worker #" + str(self.worker_id))

