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
      <div class="panel-body text-center">
        <div id="nopeers" style="display:none"><h4>TacoNET sees no peers it can browse right now.</h4></div>
        <div id="filelisting" class="text-left list-group">
        </div>
      </div>
    </div>
  </div>
</div>
  
