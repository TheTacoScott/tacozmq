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


<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Download Queue</h3></div>
      <div id="downloadqdiv" class="panel-body">
      </div>
    </div>
  </div>
</div>
<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Current Uploads</h3></div>
      <div class="panel-body text-center">
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-md-12">
    <div class="panel panel-default">
      <div class="panel-heading"><h3 class="panel-title">Completed Downloads</h3></div>
      <div class="panel-body text-center">
      </div>
    </div>
  </div>
</div>
