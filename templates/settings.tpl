%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%taco.globals.public_keys_lock.acquire()
%local_keys_copy = taco.globals.public_keys.copy()
%taco.globals.public_keys_lock.release()


%rebase templates/layout title='Settings'

<div class="modal fade bs-modal-lg" id="addPeerModal" tabindex="-1" role="dialog">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Add Peer Wizard</h4>
      </div>
      <div class="modal-body">
        <h3>Your peer will need to know the following information from you:</h3>
        <div class="input-group"><span class="input-group-addon">Your External Hostname or IP: </span><input maxlength="32" id="addpeermyhostname" type="text" class="form-control" placeholder="Your External Hostname">
          <div class="input-group-btn">
            <button id="getexternalip" class="btn btn-default" type="button"><span class="glyphicon glyphicon-refresh"></span> <span class="button-text">Get External IP</span></button>
          </div>
        </div>
        <div class="input-group"><span class="input-group-addon">Your External Port: </span><input maxlength="32" id="addpeermyport" type="text" class="form-control" placeholder="Your External Port"></div>
        <div class="input-group hide"><span class="input-group-addon">Your Server Public Key: </span><input readonly="readonly" id="addpeermyserverpublic" type="text" class="form-control" value="{{local_keys_copy['server']}}"></div>
        <div class="input-group hide"><span class="input-group-addon">Your Client Public Key: </span><input readonly="readonly" id="addpeermyclientpublic" type="text" class="form-control" value="{{local_keys_copy['client']}}"></div>
        <br>
        <h4>Below is the "Quick Connect String" your peer will need.</h4>
        <textarea id="peerneedsthis" readonly="readonly" class="form-control" rows="2"></textarea>
        <br>
        <h4>Paste the "Quick Connect String" you recieved from your peer below.</h4>
        <div class="alert alert-warning alert-dismissable hide" id='bad-connect-string'>
          <button type="button" class="close">&times;</button>
          <strong>Warning!</strong> The text below does not appear to be a valid "Quick Connect String". Have your peer create a new one, and confirm you have pasted it correctly.
        </div>

        <textarea id="ineedthis" class="form-control" rows="2"></textarea>

      </div>
      <div class="modal-footer">
        <button type="button" id="addpeercancelbutton" class="btn btn-default">Cancel</button>
        <button type="button" id="addpeerconfirmbutton" class="btn btn-primary"><span class="glyphicon glyphicon-plus"></span> Add Peer</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="downloadModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Specify Download Location</h4>
      </div>
      <div class="modal-body">
        <div class="alert alert-danger" >
          <strong>Warning!</strong> Existing downloads will not be moved. Downloads in flight will be canceled, and restarted from the beginning.
        </div>

        <div class="input-group"><span class="input-group-addon">Download Location: </span><input readonly="readonly" id="downloadloc" type="text" class="form-control"></div>
        <div class="row">
          <div class="col-md-12">
              <div id="downloadlistdiv" class="list-group">
              </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" id="downloadcancelbutton" class="btn btn-default">Cancel</button>
        <button type="button" id="downloadconfirmbutton" class="btn btn-primary"><span class="glyphicon glyphicon-ok"></span> Confirm Location</button>
      </div>
    </div>
  </div>
</div>


<div class="modal fade" id="certModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Specify Cetifcate Store Location</h4>
      </div>
      <div class="modal-body">
        <div class="alert alert-danger" >
          <strong>Warning!</strong> Existing Certs will not be moved. Don't change this setting unless you know what you're doing.
        </div>

        <div class="input-group"><span class="input-group-addon">TacoNET Certificate Store Location: </span><input readonly="readonly" id="certloc" type="text" class="form-control"></div>
        <div class="row">
          <div class="col-md-12">
              <div id="certloclistdiv" class="list-group">
              </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" id="certcancelbutton" class="btn btn-default">Cancel</button>
        <button type="button" id="certconfirmbutton" class="btn btn-primary"><span class="glyphicon glyphicon-ok"></span> Confirm Location</button>
      </div>
    </div>
  </div>
</div>



<div class="modal fade" id="addShareModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Add Share Wizard</h4>
      </div>
      <div class="modal-body">
        <div class="alert alert-warning alert-dismissable hide" id="alphanumonly">
          <button type="button" class="close">&times;</button>
          <strong>Warning!</strong> Sharename must be between 3 and 64 characters long, and must only contain alphanumeric characters, spaces, and periods. In addition, duplicate share names are not allowed.
        </div>

        <div class="input-group"><span class="input-group-addon">Share Name: </span><input maxlength="32" id="addsharename" type="text" class="form-control" placeholder="Name your share here"></div>
        <div class="input-group"><span class="input-group-addon">Share Location: </span><input readonly id="addshareloc" type="text" class="form-control"></div>
        <div id="sharebrowselistdiv" class="list-group"></div>
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
      <div class="modal-header modal-titlebar">
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
    <div class="panel-heading"><h3 class="panel-title">Settings</h3></div>
    <div class="panel-body">

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-nickname-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> Nickname must be between 3 and 64 characters long, and must only contain alphanumeric characters, spaces, and periods. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group">
        <span class="error input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="A unique nickname that you wish to be identified as on your personal TacoNET" class="glyphicon glyphicon-info-sign"></span> Your Nickname</span>
        <input autocomplete="off" id="setting-nickname" type="text" class="form-control" value="{{local_settings_copy["Nickname"]}}">
      </div>

      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The location you want to save downloaded files" class="glyphicon glyphicon-info-sign"></span> Download Location</span>
      <input autocomplete="off" id="setting-downloadlocation" readonly="readonly" type="text" class="form-control" value="{{os.path.normpath(os.path.abspath(local_settings_copy["Download Location"]))}}"><span class="input-group-btn"><button id="browsedownload" class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-appip-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> You must specify the ip in numeric form only. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The IP address that the TacoNET application server will bind to. If you are unaware of what that means, it is best to leave it as the default of '0.0.0.0'" class="glyphicon glyphicon-info-sign"></span> Application IP</span>
      <input autocomplete="off" id="setting-appip" type="text" class="form-control" value="{{local_settings_copy["Application IP"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-appport-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The application port must be a valid port number. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The PORT that the TacoNET application server will bind to. If you are unaware of what that means, it is best to leave it as the default of '9001'. This port will need be public accessible by anyone on your personal TacoNET. Router configuration may be required." class="glyphicon glyphicon-info-sign"></span> Application Port</span>
      <input autocomplete="off" id="setting-appport" type="text" class="form-control" value="{{local_settings_copy["Application Port"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-webip-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> You must specify the ip in numeric form only. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The IP address that the TacoNET web interface will bind to. If you are running TacoNET on the same system you are accessing it's web interface from, it's best to leave this as the default of '127.0.0.1', otherwise it may be wise to use '0.0.0.0'. If you are unaware of what this is, leave it the default." class="glyphicon glyphicon-info-sign"></span> Web Interface IP</span>
      <input autocomplete="off" id="setting-webip" type="text" class="form-control" value="{{local_settings_copy["Web IP"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-webport-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The web server port must be a valid port number. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The PORT that the TacoNET web server will bind to. If you are unaware of what that means, it is best to leave it as the default of '9002'. This port will typically NOT need be public accessible. This is the port you'll need to use to access TacoNET via your web browser." class="glyphicon glyphicon-info-sign"></span> Web Interface Port</span>
      <input autocomplete="off" id="setting-webport" type="text" class="form-control" value="{{local_settings_copy["Web Port"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-down-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The download limit must be expressed as a whole integer. It needs to be greater than 1. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="This is the limit TacoNET will attempt to respect when downloading content. Since ZeroMQ is a bit of socket magic, TacoNET will ATTEMPT to respect this limit." class="glyphicon glyphicon-info-sign"></span> Download Limit in KB/s</span>
      <input autocomplete="off" id="setting-downlimit" type="text" class="form-control" value="{{local_settings_copy["Download Limit"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-up-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The upload limit must be expressed as a whole integer. It needs to be greater than 1. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="This is the limit TacoNET will attempt to respect when uploading content. Since ZeroMQ is a bit of socket magic, TacoNET will ATTEMPT to respect this limit." class="glyphicon glyphicon-info-sign"></span> Upload Limit in KB/s</span>
      <input autocomplete="off" id="setting-uplimit" type="text" class="form-control" value="{{local_settings_copy["Upload Limit"]}}"></div>

      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The location your want to store your public and private certificates for use with your personal TacoNET. If you are unaware of publickey cryptography concepts, it's best to just leave this the default." class="glyphicon glyphicon-info-sign"></span> TacoNET Certificate Store</span>
      <input autocomplete="off" id="setting-certlocation" readonly="readonly" type="text" class="form-control" value="{{os.path.normpath(os.path.abspath(local_settings_copy["TacoNET Certificates Store"]))}}"><span class="input-group-btn"><button id="browsecert" class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>

    </div>
    <div class="panel-footer text-right">
      <span id="settings-saving" class="label label-info hide">Saving Settings... <img src="/static/images/ajax_loader.gif"></span>
      <span id="settings-saved" class="label label-success hide">Settings Saved</span>
      <span id="settings-unsaved" class="label label-danger hide">Unsaved Settings</span>

      <button id="save-settings" type="button" class="btn btn-default"><span class="glyphicon glyphicon-ok-sign"></span> Save Changes</button>
    </div>
  </div>
</div>
</div>

<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Shares</h3></div>

      <div id="share-add-helper" class="input-group hide">

          <span class="input-group-addon"></span>
          <input type="text" class="form-control" value="" readonly="readonly">
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
        <input type="text" class="form-control" value="{{sharelocation}}" readonly="readonly">
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
    <div class="panel-heading"><h3 class="panel-title">Peers</h3></div>

      <div id="peer-add-helper">
        <div class="panel panel-default panel-padding">
          <div class="panel-body">
            <div class="row">
              <div class="col-md-8">
              <h4><span class="glyphicon glyphicon-user"></span> Peer Nickname <small>( Local Nickname )</small></h4>
                <div class="input-group"><span class="input-group-addon">Hostname or IP</span><input autocomplete="off" type="text" class="form-control" placeholder="External Hostname" value=""></div>
                <div class="input-group"><span class="input-group-addon">Port</span><input autocomplete="off" type="text" class="form-control" placeholder="External Port" value=""></div>
                <div class="input-group"><span class="input-group-addon">Local Nickname</span><input autocomplete="off" type="text" class="form-control" placeholder="Local Nickname"></div>
                <div class="advanced-options">
                  <div class="input-group"><span class="input-group-addon">UUID</span><input autocomplete="off" type="text" class="form-control" placeholder="Local Nickname"></div>
                  <div class="input-group"><span class="input-group-addon">Client Public</span><input autocomplete="off" type="text" class="form-control" placeholder="Local Nickname"></div>
                  <div class="input-group"><span class="input-group-addon">Server Public</span><input autocomplete="off" type="text" class="form-control" placeholder="Local Nickname"></div>
                </div>
              </div>
              <div class="col-md-4 text-center">
                <button type="button" class="btn btn-danger peer-enabled-button">
                <span class="glyphicon glyphicon-stop"></span><br><span class="peer-text">Peer Disabled</span>
                </button>
                <button type="button" class="btn btn-info peer-static-button">
                <span class="glyphicon glyphicon-random"></span><br><span class="peer-text">Dynamic Hostname/IP</span>
                </button>
                <hr>
                <button type="button" class="btn btn-default toggle-advanced-peer-options"><span class="glyphicon glyphicon-wrench"></span> <span class="advanced-text">Show Advanced Settings</span></button><hr>
                <button type="button" class="btn btn-default"><span class="glyphicon glyphicon-remove"></span> Delete </button>
              </div>
            </div>
          </div>
        </div>
    </div>

    <div id='peer-listing' class="panel-body text-center">
    %if len(local_settings_copy["Peers"].keys()) == 0:
     <div id="addapeerbelow">
    %else:
     <div id="addapeerbelow" class="hide">
    %end
      <h4>You don't have any peers set up, set one up by clicking the "Add Peer" button below. <span class="glyphicon glyphicon-hand-down"></span></h4>
     </div>

    </div>
    <div class="panel-footer text-right">
      <span id="peers-saving" class="label label-info hide">Saving Settings... <img src="/static/images/ajax_loader.gif"></span>
      <span id="peers-saved" class="label label-success hide">Settings Saved</span>
      <span id="peers-unsaved" class="label label-danger hide">Unsaved Settings</span>

      <button id="add-peer" type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span> Add Peer</button>
      <button id="save-peers" type="button" class="btn btn-default"><span class="glyphicon glyphicon-ok-sign"></span> Save Changes</button>
    </div>
  </div>
</div>
</div>

