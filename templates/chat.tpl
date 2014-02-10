%rebase templates/layout title='Chat'
<div class="row">
  <div class="col-md-12">
    <div class="panel panel-info">
      <div class="panel-heading"><h3 class="panel-title">Chat</h3></div>
      <div class="panel-body">
          <div class="alert alert-success text-left local-helper hide"><span class="nick"></span><br><span class="thetime"></span><hr><span class="themsg"></span></div>
          <div class="alert alert-danger text-left remote-helper hide"><span class="nick"></span><br><span class="thetime"></span><hr><span class="themsg"></span></div>
        <div class="row text-center"> 
          <div class="col-md-12" id="chatlog">
          <img id="ajaxloader" src="/static/images/ajax-loader.gif">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<div class="row">
  <div class="col-md-1"></div>
  <div class="col-md-10">     
    <div class="input-group">
    <input type="text" id="chatbox" class="form-control">
    <span class="input-group-btn">
    <button id="chatbutton" class="btn btn-default" type="button">Send</button>
    </span>
    </div>
  </div>
  <div class="col-md-1"></div>
</div>
<br><br>
