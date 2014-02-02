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
        <table class="table table-bordered table-hover">
          <thead>
            <tr>
              <th style="width: 10%;" class="text-center">Incoming</th>
              <th style="width: 10%;" class="text-center">Outgoing</th>
              <th>Nickname</th>
              <th>Last Update</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="vertical-align:middle;color: rgb(60, 118, 61); background-color: rgb(223, 240, 216);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-ok-sign"></span></td>
              <td style="vertical-align:middle;color: rgb(169, 68, 66); background-color: rgb(242, 222, 222);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-minus-sign"></span></td>
              <td style="vertical-align:middle">NICKNAME 1</td>
              <td style="vertical-align:middle">timestamp</td>
            </tr>
            <tr>
              <td style="vertical-align:middle;color: rgb(60, 118, 61); background-color: rgb(223, 240, 216);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-ok-sign"></span></td>
              <td style="vertical-align:middle;color: rgb(138, 109, 59);background-color: rgb(252, 248, 227);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-question-sign"></span></td>
              <td style="vertical-align:middle">NICKNAME 2</td>
              <td style="vertical-align:middle">timestamp</td>
            </tr>
            <tr>
              <td style="vertical-align:middle;color: rgb(60, 118, 61); background-color: rgb(223, 240, 216);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-ok-sign"></span></td>
              <td style="vertical-align:middle;color: rgb(169, 68, 66); background-color: rgb(242, 222, 222);" class="text-center"><span style="font-size:32px;" class="glyphicon glyphicon-minus-sign"></span></td>
              <td style="vertical-align:middle">NICKNAME 3</td>
              <td style="vertical-align:middle">timestamp</td>
            </tr>
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
        <li><b>Curve PRIVATE Keys:</b> {{os.path.normpath(os.path.abspath(local_settings_copy["Curve Private Location"]))}}
        <li><b>Curve PUBLIC Keys:</b> {{os.path.normpath(os.path.abspath(local_settings_copy["Curve Public Location"]))}}
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
