%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%rebase templates/layout title='Home'
<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Peer Status</h3></div>
        <table class="table">
          <thead>
            <tr>
              <th style="width: 10%;" class="text-center">Incoming</th>
              <th style="width: 10%;" class="text-center">Outgoing</th>
              <th>Nickname</th>
            </tr>
          </thead>
          <tbody>
            %for peer_uuid in local_settings_copy["Peers"].keys():
              %if local_settings_copy["Peers"][peer_uuid]["enabled"]:
                <tr class="peerstatusrow" data-uuid="{{peer_uuid}}">
                  <td class="text-center yellow-td incomingstatus"><span style="font-size:32px;" class="glyphicon glyphicon-question-sign"></span></td>
                  <td class="text-center yellow-td outgoingstatus"><span style="font-size:32px;" class="glyphicon glyphicon-question-sign"></span></td>
                  <td class="middle-align-td"><span class="tablenick">{{local_settings_copy["Peers"][peer_uuid]["nickname"] if local_settings_copy["Peers"][peer_uuid].has_key("nickname") else "Unknown Nick"}}</span>
                  %if local_settings_copy["Peers"][peer_uuid].has_key("localnick") and len(local_settings_copy["Peers"][peer_uuid]["localnick"]) > 0:
                  <span class="glyphicon glyphicon-info-sign" data-content="Local Nickname: {{local_settings_copy["Peers"][peer_uuid]["localnick"]}}" data-placement="right" data-container="body" data-trigger="hover" data-original-title="" title=""></span>
                  %end
                  </td>
                </tr>
              %end
            %end
          </tbody>
        </table>
    </div>
  </div>
</div>
  

<div class="row">
<div class="col-md-6">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Network Settings</h3></div>
    <div class="panel-body">
      <ul>
        <li><b>My Nickname:</b> {{local_settings_copy["Nickname"]}}
        <li><b>Download Location:</b> {{os.path.normpath(os.path.abspath(local_settings_copy["Download Location"]))}}
        <li><b>Application Port:</b> {{local_settings_copy["Application Port"]}}
        <li><b>Application Bind IP:</b> {{local_settings_copy["Application IP"]}}
        <li><b>Web Interface Port:</b> {{local_settings_copy["Web Port"]}}
        <li><b>Web Interface Bind IP:</b> {{local_settings_copy["Web IP"]}}
        <li><b>Download Limit:</b> {{local_settings_copy["Download Limit"]}} KB/s
        <li><b>Upload Limit:</b> {{local_settings_copy["Upload Limit"]}} KB/s
        <li><b>Local UUID:</b> {{local_settings_copy["Local UUID"]}}
        <li><b>TacoNET Certificates Store:</b> {{os.path.normpath(os.path.abspath(local_settings_copy["TacoNET Certificates Store"]))}}
      </ul>
    </div>
  </div>
</div>
<div class="col-md-6">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Thread Status</h3></div>
    <div class="panel-body">
      <ul>
        <li><b>Dispatcher</b>
          <ul>
            <li>Last Action: {status}}
            <li>Status Updated: {taco.settings.Readable_Seconds(int(abs(time.time() - status_time)))}}
          </ul>
        <li><b>Clients</b>
          <ul>
            <li>Last Action:
            <li>Status Updated:
            <li>Client Count: ###
          </ul>
        <li><b>Socket Server</b>
          <ul>
            <li>Last Action: 
            <li>Status Updated: 
            <li>Open Sockets: ##
          </ul>
        <li><b>File System Thread</b>
          <ul>
            <li>Last Action:
            <li>Status Updated: 
            <li>Pending Search Requests: ###
          </ul>
        <li><b>bottle</b>
          <ul>
            <li>Bottle Status: --something here--
          </ul>
          
      </ul>
    </div>
  </div>
</div> <!-- END ROW -->
