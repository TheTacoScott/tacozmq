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


@bottle.post('/api.post')
def index():
  try:
    api_call = bottle.request.json
  except:
    return "0"
  if not bottle.request.json.has_key("action"): return "0"
  if not bottle.request.json.has_key("data"): return "0"
  if bottle.request.json[u"action"] == u"settingssave":
    if type(bottle.request.json[u"data"]) == type([]):
      if len(bottle.request.json[u"data"]) >= 0:
        with taco.globals.settings_lock:
          logging.info("API Access: SETTINGS -- Action: SAVE")
          for (keyname,value) in bottle.request.json[u"data"]:
            taco.globals.settings[keyname] = value
          taco.settings.Save_Settings(False)
          return "1"
  if bottle.request.json[u"action"] == u"sharesave":
    if type(bottle.request.json[u"data"]) == type([]):
      if len(bottle.request.json[u"data"]) >= 0:
        with taco.globals.settings_lock:
          logging.info("API Access: SHARE -- Action: SAVE")
          taco.globals.settings["Shares"] = []
          for (sharename,sharelocation) in bottle.request.json[u"data"]:
            taco.globals.settings["Shares"].append([sharename,sharelocation])
          taco.settings.Save_Settings(False)
          return "1"
  if bottle.request.json[u"action"] == u"peersave":
    if type(bottle.request.json[u"data"]) == type([]):
      if len(bottle.request.json[u"data"]) >= 0:
        with taco.globals.settings_lock:
          logging.info("API Access: PEER -- Action: SAVE")
          taco.globals.settings["Peers"] = {}
          for (hostname,port,localnick,peeruuid,clientpub,serverpub,dynamic,enabled) in bottle.request.json[u"data"]:
            taco.globals.settings["Peers"][unicode(peeruuid)] = {"hostname":hostname,"port": int(port),"localnick":localnick,"dynamic":int(dynamic),"enabled":int(enabled),"clientkey":clientpub,"serverkey":serverpub}
          taco.settings.Save_Settings(False)
          return "1"



  return "-1"

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
