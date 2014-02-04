import taco.bottle as bottle
import taco.settings
import taco.globals
import taco.constants
import taco.filesystem
import urllib
import re
import os,uuid
import logging
import json

#static content
@bottle.route('/static/<filename:path>')
def send_file(filename):
  return bottle.static_file(filename, root=os.path.normpath(os.getcwd() + '/static/'))

#terminate taconet
@bottle.route('/shutitdown')
def taco_page():
  taco.globals.properexit(1,1)
  return

#template routes
@bottle.route('/')
def index():
  return bottle.template('templates/home.tpl')

@bottle.route('/<name>.taco')
def taco_page(name):
  return bottle.template('templates/'+str(name)+'.tpl')


@bottle.route('/shareedit/<index>/<name>/<sharepath:path>')
def index(index,name,sharepath):
  logging.info("Editing Share UUID: " + str(index) + " " + name + " -- " + sharepath)
  with taco.globals.settings_lock:
    taco.globals.settings["Shares"][index] = [name,sharepath]
    taco.settings.Save_Settings(False)
  return "1"

@bottle.route('/sharedelete/<share_uuid>')
def index(share_uuid):
  logging.info("Deleting Share share_uuid" + str(share_uuid))
  with taco.globals.settings_lock:
    if taco.globals.settings["Shares"].has_key(share_uuid):
      del taco.globals.settings["Shares"][share_uuid]
    taco.settings.Save_Settings(False)
  return "1"

@bottle.route('/browselocaldirs/')
@bottle.route('/browselocaldirs/<browse_path:path>')
def index(browse_path="/"):
  if browse_path=="": browse_path ="/"
  browse_path = "/" + browse_path
  browse_path = unicode(browse_path)
  contents = os.listdir(browse_path)
  final_contents = []
  for item in contents:
    if os.path.isdir(os.path.join(browse_path,item)):
      final_contents.append(item)
  final_contents.sort()
  return json.dumps(final_contents)
      
  

@bottle.route('/get/<what>')
def getData(what):
  output = ""
  logging.debug("Route -- Getting your: " + what)
  if what=="uuid":
    return str(uuid.uuid4())
  if what=="ip":
    data = urllib.urlopen("http://checkip.dyndns.org/").read()
    m = re.match(r'.*Current IP Address: (.*)</body>',data)
    if m:
      output = m.group(1)
  if what =="diskfree":
    with taco.globals.settings_lock:
      down_dir = taco.globals.settings["Download Location"]
    if os.path.isdir(down_dir):
      (free,total) = taco.filesystem.Get_Free_Space(down_dir)
      if free == 0 and total == 0:
        output = 0.0
      else:
        output = free/taco.constants.GB
  return str(output)
