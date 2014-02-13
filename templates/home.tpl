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
        <table id="peerstatustable" class="table">
          <thead>
            <tr>
              <th style="width: 10%;" class="text-center">Incoming</th>
              <th style="width: 10%;" class="text-center">Outgoing</th>
              <th>Nickname</th>
              <th>Last Communication</th>
            </tr>
          </thead>
          <tbody id="peerstatustbody">
                <tr class="loadingthing"><td class="text-center" colspan="4"><img src="/static/images/ajax-loader.gif"></td></tr>
                <tr id="peerstatusrowhelper" class="hide">
                  <td class="middle-align-td text-center yellow-td incomingstatus"><span style="font-size:32px;" class="glyphicon glyphicon-question-sign"></span></td>
                  <td class="middle-align-td text-center yellow-td outgoingstatus"><span style="font-size:32px;" class="glyphicon glyphicon-question-sign"></span></td>
                  <td class="middle-align-td"><span class="tablenick"></span> <span class="localnick"></span></td>
                  <td class="middle-align-td"><strong>Incoming:</strong> <span class="lastincoming"></span><br><strong>Outgoing:</strong> <span class="lastoutgoing"></span></td>
                </tr>
          </tbody>
        </table>
    </div>
  </div>
</div>
  

<div class="row">
<div class="col-md-12">
  <div class="panel panel-info">
    <div class="panel-heading"><h3 class="panel-title">Thread Status</h3></div>
    <div class="panel-body">
      <ul>
        <li><b>Clients:</b> <span id="clientalive">UNKNOWN</span>
          <ul>
            <li>Last Action: <span id="clientstatus"></span> @ <span id="clientlast"></span>
          </ul>
        <li><b>Server:</b> <span id="serveralive">UNKNOWN</span>
          <ul>
            <li>Last Action: <span id="serverstatus"></span> @ <span id="serverlast"></span>
          </ul>
        <li><b>Webserver:</b> Running
          
      </ul>
    </div>
  </div>
</div> <!-- END ROW -->
