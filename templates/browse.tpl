%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%rebase templates/layout title='Browse'
<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Browse Peers</h3></div>
      <div class="panel-body text-center filelistingpanel">
        <div id="peercrumb" class="text-left" style="display:none"></div>
        <div id="nopeers" style="display:none"><h3>TacoNET sees no peers it can browse right now.</h3><h5>This page will auto refresh when they become browseable</h5></div>
        <div id="timedout" style="display:none"><h3>The request for this directory listing timed out.</h3><h5>You should probably return to the peer listing and try again.</h5></div>
        <img id="loaderthing" src="/static/images/ajax-loader.gif">
        <div id="peerlisting" class="text-left list-group"></div>
        <div id="sharelisting" class="text-left list-group"></div>
        <div id="dirlisting" class="text-left list-group"></div>
        </div>
      </div>
    </div>
  </div>
</div>
  
