%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%rebase templates/layout title='Settings'
<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Edit Settings</h3></div>
    <div class="panel-body">
      <div class="input-group"><span class="input-group-addon">Your Nickname</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Nickname"]}}"></div>
      <div class="input-group"><span class="input-group-addon">Download Location</span><input type="text" class="form-control" placeholder="{{os.path.normpath(os.path.abspath(local_settings_copy["Download Location"]))}}"><span class="input-group-btn"><button class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>
      <div class="input-group"><span class="input-group-addon">Application IP</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Application IP"]}}"></div>
      <div class="input-group"><span class="input-group-addon">Application Port</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Application Port"]}}"></div>
      <div class="input-group"><span class="input-group-addon">Web Interface IP</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Web IP"]}}"></div>
      <div class="input-group"><span class="input-group-addon">Web Interface Port</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Web Port"]}}"></div>
      <div class="input-group"><span class="input-group-addon">Download Limit in KB/s</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Download Limit"]}}"><span class="input-group-btn"><button class="btn btn-default" type="button"><span class="glyphicon glyphicon-cog"></span> Change</button></span></div>
      <div class="input-group"><span class="input-group-addon">Upload Limit in KB/s</span><input type="text" class="form-control" placeholder="{{local_settings_copy["Upload Limit"]}}"><span class="input-group-btn"><button class="btn btn-default" type="button"><span class="glyphicon glyphicon-cog"></span> Change</button></span></div>
      <div class="input-group"><span class="input-group-addon">Curve Private Key Location</span><input type="text" class="form-control" placeholder="{{os.path.normpath(os.path.abspath(local_settings_copy["Curve Private Location"]))}}"><span class="input-group-btn"><button class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>
      <div class="input-group"><span class="input-group-addon">Curve Public Key Location</span><input type="text" class="form-control" placeholder="{{os.path.normpath(os.path.abspath(local_settings_copy["Curve Public Location"]))}}"><span class="input-group-btn"><button class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse </button></span></div>
    </div>
    <div class="panel-footer text-center">
      <button type="button" class="btn btn-default">Save Changes</button>
    </div>
  </div>
</div>
</div>

<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Edit Shares</h3></div>
    <div class="panel-body">
    %for (name,location) in local_settings_copy["Shares"]:
      <div class="input-group">
        <span class="input-group-btn">
         <button class="btn btn-default" type="button"><span class="glyphicon glyphicon-pencil"></span> {{name}}</button>
        </span>
        <input type="text" class="form-control" placeholder="{{location}}">
        <div class="input-group-btn">
          <button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button>
          <button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-remove"></span> Delete</button>
        </div>
      </div>
    %end
      <div id="share-add-helper" class="input-group hide">
        <span class="input-group-btn">
         <button class="btn btn-default" type="button"><span class="glyphicon glyphicon-pencil"></span> New Share Name</button>
        </span>
        <input type="text" class="form-control" placeholder="">
        <div class="input-group-btn">
          <button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button>
          <button class="btn btn-default" tabindex="-1" type="button"><span class="glyphicon glyphicon-remove"></span> Delete</button>
        </div>
      </div>

    </div>
    <div class="panel-footer text-center">
      <button type="button" class="btn btn-default">Add Share</button>
      <button type="button" class="btn btn-default">Save Changes</button>
    </div>
  </div>
</div>
</div>

<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Edit Peers</h3></div>
    <div class="panel-body">
    </div>
    <div class="panel-footer text-center">
      <button type="button" class="btn btn-default">Add Peer</button>
      <button type="button" class="btn btn-default">Save Changes</button>
    </div>
  </div>
</div>
</div>

