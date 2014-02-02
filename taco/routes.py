import taco.bottle as bottle
import taco.settings
import taco.globals
import taco.constants
import taco.filesystem
import urllib
import re
import os
import logging

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

#web api to add a peer or share
@bottle.route('/add/<what>')
@bottle.route('/add/<what>/<uuid>')
def index(what, uuid = None):
  if what=="peer":
    taco.settings.Add_Peer(uuid)
    return "1"
  if what=="share":
    taco.settings.Add_Share("")
    return "1"

@bottle.route('/delete/<what>/<option>')
def index(what,option):
  if what=="peer":
    taco.settings.Delete_Peer(option)
    return "1"
  if what=="share":
    taco.settings.Delete_Share(int(option))
    return "1"


@bottle.route('/get/<what>')
def getData(what):
  output = ""
  logging.debug("Route -- Getting your: " + what)
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
