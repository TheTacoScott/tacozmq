%import taco.globals
%import os

%taco.globals.settings_lock.acquire()
%local_settings_copy = taco.globals.settings.copy()
%taco.globals.settings_lock.release()

%rebase templates/layout title='Transfers'
<div class="modal fade" id="removeModal" tabindex="-1" role="dialog">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Remove from download queue?</h4>
      </div>
      <div class="modal-body">
        <span class="glyphicon glyphicon-file" style="margin-right: 10px;"></span><span id="removefilename"></span><span id="removesize"></span><br>
        <span class="glyphicon glyphicon-folder-open" style="margin-right: 10px;"></span><span id="removesharedir"></span>
      </div>
      <div class="modal-footer">
        <button type="button" id="removecancelbutton" class="btn btn-default" data-dismiss="modal">Cancel</button>
        <button type="button" id="removebutton" class="btn btn-danger"><span class="glyphicon glyphicon-remove"></span> Remove</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="removeCompletedModal" tabindex="-1" role="dialog">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header modal-titlebar">
        <h4 class="modal-title">Clear the list of completed downloads?</h4>
      </div>
      <div class="modal-body">
       <h3>Are you sure you want to clear your download history?</h3>
      </div>
      <div class="modal-footer">
        <button type="button" id="completedremovecancelbutton" class="btn btn-default" data-dismiss="modal">Cancel</button>
        <button type="button" id="completedremovebutton" class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span> Clear</button>
      </div>
    </div>
  </div>
</div>



<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Download Queue <span id="hoverpaused" class="hide" style="float:right"><span class="glyphicon glyphicon-time"></span> Automatic Update Paused while hovering/dragging.</span></h3></div>
      <div id="downloadqempty" class="text-center hide"><h3>You don't have any pending downloads.</h3><h6>Add something to your download queue, once they are queued they will appear here.</h6></div>
      <div id="downloadqdiv" class="panel-body">
      </div>
    </div>
  </div>
</div>
<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Current Uploads</h3></div>
      <div id="uploadqempty" class="text-center hide"><h3>You don't have anyone downloading for you.</h3><h6>When uploads are in progress they will appear here.</h6></div>
      <div id="uploaddiv" class="panel-body text-center">
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="panel panel-default">
      <div class="panel-heading"><h3 class="panel-title">Downloads History</h3></div>
      <div id="completedqempty" class="text-center hide"><h3>You don't have any download history.</h3><h6>Add something to your download queue, when it is done it will appear here.</h6></div>
      <div id="completedqdiv" class="panel-body text-center">

      </div>
      <div id="completedfooter" class="panel-footer text-right hide">
        <button type="button" id="completedfooterremovebutton" class="btn btn-danger"><span class="glyphicon glyphicon-trash"></span> Clear History</button>
      </div>
    </div>
  </div>
</div>
