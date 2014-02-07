%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%rebase templates/layout title='Settings'
<div class="modal fade" id="addShareModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title">Add Share</h4>
      </div>
      <div class="modal-body">
        <div class="alert alert-warning alert-dismissable hide" id="alphanumonly">
          <button type="button" class="close">&times;</button>
          <strong>Warning!</strong> Sharename must be between 3 and 64 characters long, and must only contain alphanumeric characters, spaces, and periods.
        </div>

        <div class="input-group"><span class="input-group-addon">Share Name: </span><input maxlength="32" id="addsharename" type="text" class="form-control" placeholder="Name your share here"></div>
        <div class="input-group"><span class="input-group-addon">Share Location: </span><input readonly id="addshareloc" type="text" class="form-control"></div>
        <div class="row">
          <div class="col-md-12">
              <h5>Share Location</h5>
              <div id="sharebrowselistdiv" class="list-group">
              </div>
          </div> 
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" id="addsharecancelbutton" class="btn btn-default">Cancel</button>
        <button type="button" id="addshareconfirmbutton" class="btn btn-primary"><span class="glyphicon glyphicon-plus"></span> Add Share</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="deleteShareModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h4 class="modal-title">Delete Share</h4>
      </div>
      <div class="modal-body">
      </div>
      <div class="modal-footer">
        <button type="button" id="deletesharecancelbutton" class="btn btn-default" data-dismiss="modal">Cancel</button>
        <button type="button" id="deleteshareconfirmbutton" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> Delete Share</button>
      </div>
    </div>
  </div>
</div>



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
    <div class="panel-footer text-right">
      <button type="button" class="btn btn-default">Save Changes</button>
    </div>
  </div>
</div>
</div>

<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Edit Shares</h3></div>

      <div id="share-add-helper" class="input-group hide">

          <span class="input-group-addon"></span>
          <input type="text" class="form-control" placeholder="" value="" readonly="readonly">
          <div class="input-group-btn">
            <button data-type="share" data-action="delete" data-name="" class="btn btn-default" type="button"><span class="glyphicon glyphicon-remove"></span> Delete</button>
          </div>

      </div>
    <div id="share-listing" class="panel-body text-center">
    %if len(local_settings_copy["Shares"]) == 0:
     <div id="addasharebelow">
    %else:
     <div id="addasharebelow" class="hide">
    %end
      <h4>You don't have any shares set up, set one up by clicking the "Add Share" button below. <span class="glyphicon glyphicon-hand-down"></span></h4>
     </div>

    %for (sharename,sharelocation) in local_settings_copy["Shares"]:
      <div class="input-group">
        <span class="input-group-addon">{{sharename}}</span>
        <input type="text" class="form-control" placeholder="{{sharelocation}}" value="{{sharelocation}}" readonly="readonly">
        <div class="input-group-btn">
          <button data-type="share" data-action="delete" data-name="{{sharename}}" class="btn btn-default" type="button"><span class="glyphicon glyphicon-remove"></span> Delete</button>
        </div>
      </div>
    %end
    </div>
    <div class="panel-footer text-right">
      <span id="shares-saving" class="label label-info hide">Saving Settings... <img src="/static/images/ajax_loader.gif"></span>
      <span id="shares-saved" class="label label-success hide">Settings Saved</span>
      <span id="shares-unsaved" class="label label-danger hide">Unsaved Settings</span>
      <button id="add-share" type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span> Add Share</button>
      <button id="save-shares" type="button" class="btn btn-default"><span class="glyphicon glyphicon-ok-sign"></span> Save Changes</button>
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
    <div class="panel-footer text-right">
      <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span> Add Peer</button>
      <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-ok-sign"></span> Save Changes</button>
    </div>
  </div>
</div>
</div>

