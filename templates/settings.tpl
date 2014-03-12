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
        <div class="input-group"><span class="input-group-addon"><span class="glyphicon glyphicon-info-sign" data-content="This is the publicly accessible IP or Hostname of your {{taco.constants.APP_NAME}} application instance." data-placement="right" data-container="#addPeerModal" data-trigger="hover" data-original-title="" title=""></span> Your External Hostname or IP: </span><input maxlength="32" id="addpeermyhostname" type="text" class="form-control" placeholder="Your External Hostname">
          <div class="input-group-btn">
            <button id="getexternalip" class="btn btn-default" type="button"><span class="glyphicon glyphicon-refresh"></span> <span class="button-text">Get External IP</span></button>
          </div>
        </div>
        <div class="input-group"><span class="input-group-addon"><span class="glyphicon glyphicon-info-sign" data-content="This is the publicly accessible port of your {{taco.constants.APP_NAME}} application instance. It must be forwarded from your router." data-placement="right" data-container="#addPeerModal" data-trigger="hover" data-original-title="" title=""></span> Your External Port: </span><input maxlength="32" id="addpeermyport" type="text" class="form-control" placeholder="Your External Port"></div>
        <div class="input-group hide"><span class="input-group-addon">Your Server Public Key: </span><input readonly="readonly" id="addpeermyserverpublic" type="text" class="form-control" value="{{local_keys_copy['server']}}"></div>
        <div class="input-group hide"><span class="input-group-addon">Your Client Public Key: </span><input readonly="readonly" id="addpeermyclientpublic" type="text" class="form-control" value="{{local_keys_copy['client']}}"></div>
        <div class="input-group hide"><span class="input-group-addon">Your UUID: </span><input readonly="readonly" id="addpeermyuuid" type="text" class="form-control" value="{{local_settings_copy['Local UUID']}}"></div>
        <br>
        <h4>Below is the "Quick Connect String" your peer will need.</h4>
        <textarea id="peerneedsthis" readonly="readonly" class="form-control" rows="2"></textarea>
        <br>
        <h4>Paste the "Quick Connect String" you recieved from your peer below.</h4>
        <div class="alert alert-warning alert-dismissable hide" id='bad-connect-string'>
          <button type="button" class="close">&times;</button>
          <strong>Warning!</strong> The text below does not appear to be a valid "Quick Connect String". Have your peer create a new one, and confirm you have pasted it correctly.<br>
          <strong>Error:</strong> <span class="exact-error"></span>
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

        <div class="input-group"><span class="input-group-addon">Certificate Store Location: </span><input readonly="readonly" id="certloc" type="text" class="form-control"></div>
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

<div class="modal fade" id="deletePeerModal" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Delete Peer</h4>
      </div>
      <div class="modal-body">
      </div>
      <div class="modal-footer">
        <button type="button" id="deletepeercancelbutton" class="btn btn-default" data-dismiss="modal">Cancel</button>
        <button type="button" id="deletepeerconfirmbutton" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> Delete Peer</button>
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
        <span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="A unique nickname that you wish to be identified as on your personal {{taco.constants.APP_NAME}} instance." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Your Nickname</span></span>
        <input autocomplete="off" id="setting-nickname" type="text" class="form-control" value="{{local_settings_copy["Nickname"]}}">
      </div>

      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The location you want to save downloaded files" class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Download Location</span></span>
      <input autocomplete="off" id="setting-downloadlocation" readonly="readonly" type="text" class="form-control" value="{{os.path.normpath(os.path.abspath(local_settings_copy["Download Location"]))}}"><span class="input-group-btn"><button id="browsedownload" class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-appip-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> You must specify the ip in numeric form only. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The IP address that the {{taco.constants.APP_NAME}} application server will bind to. If you are unaware of what that means, it is best to leave it as the default of '0.0.0.0'" class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Application IP</span></span>
      <input autocomplete="off" id="setting-appip" type="text" class="form-control" value="{{local_settings_copy["Application IP"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-appport-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The application port must be a valid port number. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The PORT that the {{taco.constants.APP_NAME}} application server will bind to. If you are unaware of what that means, it is best to leave it as the default of '9001'. This port will need be public accessible by anyone on your personal {{taco.constants.APP_NAME}} instance. Router configuration may be required." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Application Port</span></span>
      <input autocomplete="off" id="setting-appport" type="text" class="form-control" value="{{local_settings_copy["Application Port"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-webip-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> You must specify the ip in numeric form only. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The IP address that the {{taco.constants.APP_NAME}} web interface will bind to. If you are running {{taco.constants.APP_NAME}} on the same system you are accessing it's web interface from, it's best to leave this as the default of '127.0.0.1', otherwise it may be wise to use '0.0.0.0'. If you are unaware of what this is, leave it the default." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Web Interface IP</span></span>
      <input autocomplete="off" id="setting-webip" type="text" class="form-control" value="{{local_settings_copy["Web IP"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-webport-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The web server port must be a valid port number. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The PORT that the {{taco.constants.APP_NAME}} web server will bind to. If you are unaware of what that means, it is best to leave it as the default of '9002'. This port will typically NOT need be public accessible. This is the port you'll need to use to access {{taco.constants.APP_NAME}} via your web browser." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Web Interface Port</span></span>
      <input autocomplete="off" id="setting-webport" type="text" class="form-control" value="{{local_settings_copy["Web Port"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-down-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The download limit must be expressed as a whole integer. It needs to be greater than 1. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="This is the limit {{taco.constants.APP_NAME}} will attempt to respect when downloading content. Since ZeroMQ is a bit of socket magic, {{taco.constants.APP_NAME}} will ATTEMPT to respect this limit." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Download Limit in KB/s</span></span>
      <input autocomplete="off" id="setting-downlimit" type="text" class="form-control" value="{{local_settings_copy["Download Limit"]}}"></div>

      <div class="alert alert-warning alert-dismissable alert-tweak hide" id="setting-up-alert"><button type="button" class="close">&times;</button><strong>Warning!</strong> The upload limit must be expressed as a whole integer. It needs to be greater than 1. <span class="glyphicon glyphicon-hand-down"></span></div>
      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="This is the limit {{taco.constants.APP_NAME}} will attempt to respect when uploading content. Since ZeroMQ is a bit of socket magic, {{taco.constants.APP_NAME}} will ATTEMPT to respect this limit." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Upload Limit in KB/s</span></span>
      <input autocomplete="off" id="setting-uplimit" type="text" class="form-control" value="{{local_settings_copy["Upload Limit"]}}"></div>

      <div class="input-group"><span class="input-group-addon"><span data-trigger="hover" data-container="body" data-placement="right" data-content="The location your want to store your public and private certificates for use with your personal {{taco.constants.APP_NAME}} instance. If you are unaware of publickey cryptography concepts, it's best to just leave this the default." class="glyphicon glyphicon-info-sign"></span><span class="iga-fixed-width">Certificate Store</span></span>
      <input autocomplete="off" id="setting-certlocation" readonly="readonly" type="text" class="form-control" value="{{os.path.normpath(os.path.abspath(local_settings_copy["TacoNET Certificates Store"]))}}"><span class="input-group-btn"><button id="browsecert" class="btn btn-default" type="button"><span class="glyphicon glyphicon-folder-open"></span>&nbsp Browse</button></span></div>

    </div>
    <div class="panel-footer text-right">
      <span id="settings-saving" class="label label-info hide">Saving Settings... <img src="/static/images/ajax_loader.gif"></span>
      <span id="settings-saved" class="label label-success hide">Settings Saved</span>
      <span id="settings-unsaved" class="label label-danger hide">Unsaved Settings</span>
      <span id="settings-errors" class="label label-danger hide">You have errors your must correct</span>
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

      <div id="peer-add-helper" class='hide'>
        <div class="panel panel-default panel-padding red-bg peerblock">
          <div class="panel-body">
            <div class="row">
              <div class="col-md-8">
                <h4><span class="glyphicon glyphicon-user"></span> <span class="peernick">Peer Nickname</span></h4>

                <div class="alert alert-warning alert-dismissable alert-tweak hide peerhostbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The hostname you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Hostname or IP</span></span><input autocomplete="off" type="text" class="form-control peerhost" placeholder="External Hostname" value=""><span class="input-group-addon">Dynamic? <input class='peerdynamic' type="checkbox"></input></span></div>

                <div class="alert alert-warning alert-dismissable alert-tweak hide peerportbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The port you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Port</span></span><input autocomplete="off" type="text" class="form-control peerport" placeholder="External Port" value=""></div>

                <div class="alert alert-warning alert-dismissable alert-tweak hide peernickbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The local nickname you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Port</span>Local Nickname</span></span><input autocomplete="off" type="text" class="form-control peerlocalnick" placeholder="Local Nickname"></div>
                <div class="advanced-options">
                
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peeruuidbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The UUID you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>UUID</span></span><input autocomplete="off" type="text" class="form-control peeruuid" placeholder="UUID"></div>
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peerclientbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The Client Public Key you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Client Public</span></span><input autocomplete="off" type="text" class="form-control peerclient" placeholder=""></div>
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peerserverbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The Server Public Key you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Server Public</span></span><input autocomplete="off" type="text" class="form-control peerserver" placeholder=""></div>
                </div>
              </div>
              <div class="col-md-4 text-center">
                <button style="width: 120px" type="button" class="btn btn-default peer-enabled-button">
                <span class="glyphicon glyphicon-play"></span><br><span class="peer-text">Enable Peer</span>
                </button>
                <hr>
                <button type="button" class="btn btn-default toggle-advanced-peer-options"><span class="glyphicon glyphicon-wrench"></span> <span class="advanced-text">Show Advanced Settings</span></button><hr>
                <button type="button" class="btn btn-default delete-peer"><span class="glyphicon glyphicon-remove"></span> Delete </button>
              </div>
            </div>
          </div>
        </div>
    </div>

    <div id='peer-listing' class="panel-body">
    %if len(local_settings_copy["Peers"].keys()) == 0:
     <div id="addapeerbelow" class="text-center">
    %else:
     <div id="addapeerbelow" class="text-center hide">
    %end
      <h4>You don't have any peers set up, set one up by clicking the "Add Peer" button below. <span class="glyphicon glyphicon-hand-down"></span></h4>
     </div>
    %for p_uuid in local_settings_copy["Peers"].keys():
      %add_class = "red-bg"
       <div class="panel panel-default panel-padding {{"green-bg" if local_settings_copy["Peers"][p_uuid]["enabled"] else "red-bg"}} peerblock">
          <div class="panel-body">
            <div class="row">
              <div class="col-md-8">
                <h4><span class="glyphicon glyphicon-user"></span> <span class="peernick">{{local_settings_copy["Peers"][p_uuid]["nickname"] if local_settings_copy["Peers"][p_uuid].has_key("nickname") else "Peer Nickname"}}</span></h4>

                <div class="alert alert-warning alert-dismissable alert-tweak hide peerhostbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The hostname you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Hostname or IP</span></span><input autocomplete="off" type="text" class="form-control peerhost" placeholder="External Hostname" value="{{local_settings_copy["Peers"][p_uuid]["hostname"]}}"><span class="input-group-addon">Dynamic? <input class='peerdynamic' type="checkbox" {{"checked='yes'" if local_settings_copy["Peers"][p_uuid]["dynamic"] else ""}}></input></span></div>
                
                <div class="alert alert-warning alert-dismissable alert-tweak hide peerportbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The port you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Port</span></span><input autocomplete="off" type="text" class="form-control peerport" placeholder="External Port" value="{{local_settings_copy["Peers"][p_uuid]["port"]}}"></div>
                <div class="alert alert-warning alert-dismissable alert-tweak hide peernickbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The local nickname you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Local Nickname</span></span><input autocomplete="off" type="text" class="form-control peerlocalnick" placeholder="Local Nickname" value="{{local_settings_copy["Peers"][p_uuid]["localnick"]}}"></div>
                <div class="advanced-options">
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peeruuidbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The UUID you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>UUID</span></span><input autocomplete="off" type="text" class="form-control peeruuid" placeholder="UUID" value="{{p_uuid}}"></div>
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peerclientbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The Client Public Key you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Client Public</span></span><input autocomplete="off" type="text" class="form-control peerclient" placeholder="" value="{{local_settings_copy["Peers"][p_uuid]["clientkey"]}}"></div>
                  <div class="alert alert-warning alert-dismissable alert-tweak hide peerserverbad"><button type="button" class="close">&times;</button><strong>Warning!</strong> The Server Public Key you have specified is invalid.<span class="glyphicon glyphicon-hand-down"></span></div>
                  <div class="input-group"><span class="input-group-addon"><span class='iga-fixed-width'>Server Public</span></span><input autocomplete="off" type="text" class="form-control peerserver" placeholder="" value="{{local_settings_copy["Peers"][p_uuid]["serverkey"]}}"></div>
                </div>
              </div>
              <div class="col-md-4 text-center">
                <button style="width: 120px" type="button" class="btn btn-default peer-enabled-button">
                %if local_settings_copy["Peers"][p_uuid]["enabled"]:
                  <span class="glyphicon glyphicon-stop"></span><br><span class="peer-text">Disable Peer</span>
                %else:
                  <span class="glyphicon glyphicon-play"></span><br><span class="peer-text">Enable Peer</span>
                %end
                </button>
                <hr>
                <button type="button" class="btn btn-default toggle-advanced-peer-options"><span class="glyphicon glyphicon-wrench"></span> <span class="advanced-text">Show Advanced Settings</span></button><hr>
                <button type="button" class="btn btn-default delete-peer"><span class="glyphicon glyphicon-remove"></span> Delete </button>
              </div>
            </div>
          </div>
        </div>
    %end
    </div>
    <div class="panel-footer text-right">
      <span id="peers-saving" class="label label-info hide">Saving Settings... <img src="/static/images/ajax_loader.gif"></span>
      <span id="peers-saved" class="label label-success hide">Settings Saved</span>
      <span id="peers-unsaved" class="label label-danger hide">Unsaved Settings</span>
      <span id="peers-errors" class="label label-danger hide">You have errors your must correct</span>

      <button id="add-peer" type="button" class="btn btn-default"><span class="glyphicon glyphicon-plus"></span> Add Peer</button>
      <button id="save-peers" type="button" class="btn btn-default"><span class="glyphicon glyphicon-ok-sign"></span> Save Changes</button>
    </div>
  </div>
</div>
</div>

