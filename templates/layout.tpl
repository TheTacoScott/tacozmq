%import taco.constants
%import random

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="/static/images/favicon.ico">

    <title>{{taco.constants.APP_NAME}} v{{taco.constants.APP_VERSION}} - {{title or 'Home'}}</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <link href="/static/css/taconet-default.css" rel="stylesheet">

    <script src="/static/js/jquery-1.11.0.min.js"></script>
    <script src="/static/js/jquery-ui.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="/static/js/main.js"></script>
    <script type="text/javascript" src="/static/js/{{title.lower()}}.js"></script>
  
  </head>

  <body>
    <div class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/"><img src="/static/images/taco.png" height="16"> <b>TacoNET</b></a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="{{"active" if title=="Home" else ""}}"><a href="/"><i class="glyphicon glyphicon-home"></i><span class="navlink">Home</span></a></li>
            <li class="{{"active" if title=="Chat" else ""}}"><a href="/chat.taco"><i class="glyphicon glyphicon-comment"></i><span class="navlink">Chat</span></a></li>
            <li class="{{"active" if title=="Transfers" else ""}}"><a href="/transfers.taco"><i class="glyphicon glyphicon-transfer"></i><span class="navlink">Transfers</span></a></li>
            <li class="{{"active" if title=="Search" else ""}}"><a href="/search.taco"><i class="glyphicon glyphicon-search"></i><span class="navlink">Search</span></a></li>
            <li class="{{"active" if title=="Browse" else ""}}"><a href="/browse.taco"><i class="glyphicon glyphicon-folder-open"></i><span style="margin-left: 5px" class="navlink">Browse</span></a></li>
            <li class="{{"active" if title=="Settings" else ""}}"><a href="/settings.taco"><i class="glyphicon glyphicon-edit"></i><span class="navlink">Settings</span></a></li>
            <li class="{{"active" if title=="Help" else ""}}"><a target="_blank" href="https://github.com/withorwithoutgod/taconet/wiki"><i class="glyphicon glyphicon-info-sign"></i><span class="navlink">Help</span></a></li> 
            <li class="navlink-nohide"><a href="."><i class="glyphicon glyphicon-arrow-down"></i> <span id="downloadspeed"></span></a></li>
            <li class="navlink-nohide"><a href="."><i class="glyphicon glyphicon-arrow-up"></i> <span id="uploadspeed"></span></a></li>

          </ul>
      
      <ul class="nav navbar-nav navbar-right">
      <li class="dropdown">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="glyphicon glyphicon-off"></i><span class="navlink">Shutdown</span> <b class="caret"></b></a>
        <ul class="dropdown-menu">
        <li><a href="/shutitdown.taco">Confirm Shutdown</a></li>
        </ul>
      </li>
      </ul>
        </div>
      </div>
    </div>

    <div class="container">
    <div id="apialert" class="alert alert-danger hide"><strong>Error!</strong> The backend TacoNET process does not appear to be running. Please restart it and then <a href="#" onclick="location.reload();">refresh this page</a>.</div>
    %include
    </div>
  </body>
  <footer class="text-center">
    <div class="panel panel-default">
      <div class="panel-body">
        %random.shuffle(taco.constants.APP_AUTHOR)
        <small><small>
        {{taco.constants.APP_NAME}} v{{taco.constants.APP_VERSION}} "{{taco.constants.APP_CODE_NAME}}" -- {{taco.constants.APP_STAGE}} --  MIT License -- Written by {{" and ".join(taco.constants.APP_AUTHOR)}}<br>
        {{random.choice(taco.constants.APP_TAGLINE)}}
        </small></small>
      </div>
    </div>
  </footer>
</html>

