var nick_pattern = new RegExp("^[a-zA-Z0-9\. ]{3,48}$");
var ip_pattern = new RegExp("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
var port_pattern = new RegExp("^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$");
var limit_pattern = new RegExp("^[1-9][0-9]+$");
var z85_pattern = /^[\.:\+=\^!/\*\?&<>\(\)\[\]\{\}@%\$#a-zA-Z0-9-]{40}$/;
var uuid_pattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function Download_Browse()
{
  Share_Browse("/",$("#downloadlistdiv"),$("#downloadloc"))
  $("#downloadloc").val("/");
  $("button[id='downloadconfirmbutton']").unbind("click").click(function() { 
    $("#setting-downloadlocation").val($("#downloadloc").val());
    $("#setting-downloadlocation").addClass("input-changed");
    $("span[id='settings-unsaved']").removeClass("hide");
    $('#downloadModal').modal('hide');

  });
  $("button[id='downloadcancelbutton']").unbind("click").click(function() { $("#downloadlistdiv").scrollTop(0); $('#downloadModal').modal('hide');  });
  $('#downloadModal').modal();
}

function Cert_Browse()
{
  Share_Browse("/",$("#certloclistdiv"),$("#certloc"))
  $("#certloc").val("/");
  $("button[id='certconfirmbutton']").unbind("click").click(function() { 
    $("#setting-certlocation").val($("#certloc").val());
    $("#setting-certlocation").addClass("input-changed");
    $("span[id='settings-unsaved']").removeClass("hide");
    $('#certModal').modal('hide'); 
  });
  $("button[id='certcancelbutton']").unbind("click").click(function() { $("#certloclistdiv").scrollTop(0); $('#certModal').modal('hide');  });
  $('#certModal').modal();
}


function Share_Browse($browsedir,$target,$target2)
{
  $.getJSON( "/browselocaldirs/" + $browsedir, function( data ) 
  {
    var items = [];
    if ($browsedir != "" && $browsedir != "/") {     
      var updir = $browsedir.split("/");
      updir.pop()
      updir = updir.join("/");
      items.push('<a href="#" data-browsedir="'+updir+'" class="list-group-item"><span class="glyphicon glyphicon-arrow-left"></span> &nbsp.. [BACK]</a>');
    }
    $.each(data,function(key,val)
    {
      if ($browsedir=="/") { $browsedir=""; }
      items.push('<a href="#" data-browsedir="'+$browsedir+'/'+val+'" class="list-group-item"><span class="glyphicon glyphicon-folder-open"></span> &nbsp'+val+'</a>');
    });
    $target.html(items.join(""));
    if ($browsedir=="") { $browsedir = "/"; }
    $target2.val($browsedir);
    $target.find("a[class='list-group-item']").unbind("click").click(function()
    {
      $browsedir = $(this).data("browsedir");
      Share_Browse($browsedir,$target,$target2);
    });
    $target.scrollTop(0);
  });
}
function Confirm_Add_Share()
{
  var pattern = new RegExp("^[a-zA-Z0-9\. ]{3,64}$");
  var $sharename = $("input[id='addsharename']").val();
  var $sharelocation = $("input[id='addshareloc']").val();
  var $valid_name = true;
  $("button[data-type='share'][data-action='delete']").each(function () {
   if ($(this).data("name").toLowerCase() == $sharename.toLowerCase())  { $valid_name = false; }
  });
  if (pattern.test($sharename) && $valid_name)
  { 
    $("div[id='share-add-helper'] span:first").html($sharename);
    $("div[id='share-add-helper'] input:first").val($sharelocation);
    $("div[id='share-add-helper']").clone().removeAttr("id").removeClass("hide").attr("id","TEMPSHARE").appendTo("div[id='share-listing']");
    $("div[id='TEMPSHARE'] button[data-action='delete']").data("name",$sharename);
    $("div[id='TEMPSHARE'] button[data-action='edit']").data("name",$sharename);
    $("div[id='TEMPSHARE']").removeAttr("id");
    Set_Up_Delete_Share();
    $('#addShareModal').modal('hide');
    $("div[id='addasharebelow']").addClass("hide");
    $("span[id='shares-unsaved']").removeClass("hide"); 
  }
  else
  {
    $("#addShareModal .modal-body div[id='alphanumonly']").removeClass('hide');
  }
  //setTimeout(function() { $("#addShareModal .modal-body div[id='alphanumonly']").fadeOut(); },5000);  
}
function Add_Share()
{
  //$("div[id='share-add-helper']").clone().removeAttr("id").removeClass("hide").appendTo("div[id='share-listing']");
  Share_Browse("/",$("#sharebrowselistdiv"),$("#addshareloc"))
  $("#addShareModal .modal-body div[id='alphanumonly']").addClass('hide');
  $("#addshareloc").val("/");
  $("#addsharename").val("");
  $("button[id='addshareconfirmbutton']").unbind("click").click(function() { Confirm_Add_Share(); });
  $("button[id='addsharecancelbutton']").unbind("click").click(function() { $("#sharebrowselistdiv").scrollTop(0); $('#addShareModal').modal('hide');  });
  $('#addShareModal').modal();
}

function Delete_Share($id)
{
  var $sharename = $id.data("name");
  var $fadeoutdiv = $id.parent().parent();
  $('#deleteShareModal .modal-body').html("<h5>Delete sharename: <b>"+$sharename+"</b>?</h5>");
  $('#deleteShareModal').modal();
  $("button[id='deleteshareconfirmbutton']").unbind("click").click(function() { Confirm_Delete_Share($sharename,$fadeoutdiv); });
}
function Confirm_Delete_Share($name,$div)
{
  $('#deleteShareModal').modal('hide');
  $div.fadeOut(1000,function() { $(this).remove(); if ($("div[id='share-listing'] div[class='input-group']").length == 0) { $("div[id='addasharebelow']").removeClass("hide"); } });
  $("span[id='shares-unsaved']").removeClass("hide");
  
}

function Save_Shares()
{

  $("button[id='save-shares']").prop("disabled",true);
  $("span[id='shares-saving']").removeClass("hide");
  var $api_action = {"action":"sharesave","data":[]};

  $("div[id='share-listing'] div[class='input-group']").each(function()
  {
    var $sharename = $(this).find("span:first").html();
    var $sharelocation = $(this).find("input[type='text']").val();
    if ($sharelocation != "" && $sharename != "") 
    {
      $api_action["data"].push([$sharename,$sharelocation]);
    }
  });
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  { 
    if (data==1) { 
      $("span[id='shares-unsaved']").addClass("hide");
      $("span[id='shares-saving']").addClass("hide");
      $("span[id='shares-saved']").hide().removeClass("hide").fadeIn();
      setTimeout(function() 
        { 
          $("span[id='shares-saved']").fadeOut(1000,function() 
          {
            $("button[id='save-shares']").prop("disabled",false);
            if ($("div[id='share-listing'] div[class='input-group']").length == 0) { $("div[id='addasharebelow']").removeClass("hide"); }
          });
        },2000);
    }    
  }
  }); 
}

function Set_Up_Delete_Share()
{
 $("button[data-type='share'][data-action='delete']").unbind("click").click(function() { Delete_Share($(this)); });
 $("button[data-type='share'][data-action='delete']").prop("disabled",false);
}
function Save_Peers()
{
  var $api_action = {"action":"peersave","data":[]};
  $("span[id='peers-saving']").removeClass("hide"); 
  $("span[id='peers-errors']").addClass("hide");
  $("#peer-listing .peerblock .input-error").removeClass("input-error");
  $("#peer-listing .peerblock .alert").addClass("hide");
  $("#peer-listing .peerblock").each(function() {
   $host = $(this).find(".peerhost").val();
   $port = $(this).find(".peerport").val();
   $nick = $(this).find(".peerlocalnick").val();
   $uuid = $(this).find(".peeruuid").val();
   $client = $(this).find(".peerclient").val();
   $server = $(this).find(".peerserver").val();
   $dynamic = $(this).find(".peerdynamic").is(":checked");
   $enabled = $(this).find(".peer-enabled-button span").hasClass("glyphicon-stop");

   if ($host.length==0) { $(this).find(".peerhost").removeClass("input-changed").addClass("input-error"); $(this).find(".peerhostbad").removeClass("hide"); }
   if (!port_pattern.test($port)) { $(this).find(".peerport").removeClass("input-changed").addClass("input-error"); $(this).find(".peerportbad").removeClass("hide"); }
   if (!nick_pattern.test($nick) && $nick != "") { $(this).find(".peerlocalnick").removeClass("input-changed").addClass("input-error"); $(this).find(".peernickbad").removeClass("hide"); }
   if (!uuid_pattern.test($uuid)) { $(this).find(".advanced-options").slideDown(); $(this).find(".peeruuid").removeClass("input-changed").addClass("input-error"); $(this).find(".peeruuidbad").removeClass("hide"); }
   if (!z85_pattern.test($client)) { $(this).find(".advanced-options").slideDown(); $(this).find(".peerclient").removeClass("input-changed").addClass("input-error"); $(this).find(".peerclientbad").removeClass("hide"); }
   if (!z85_pattern.test($server)) { $(this).find(".advanced-options").slideDown(); $(this).find(".peerserver").removeClass("input-changed").addClass("input-error"); $(this).find(".peerserverbad").removeClass("hide"); }

   $api_action["data"].push([$host,$port,$nick,$uuid,$client,$server,$dynamic,$enabled]);
  });
  if ($("#peer-listing .input-error").length == 0)
  {
     $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
     {
      if (data==1) {
        $("span[id='peers-unsaved']").addClass("hide");
        $("span[id='peers-saving']").addClass("hide");
        $("span[id='peers-saved']").hide().removeClass("hide").fadeIn();
        $("#peer-listing .peerblock .input-changed").removeClass("input-changed");
        setTimeout(function()
          {
            $("span[id='peers-saved']").fadeOut(1000,function()
            {
              $("button[id='save-peers']").prop("disabled",false);
            });
          },2000);
      }
    }
    });
  }
  else
  {
    $("span[id='peers-saving']").addClass("hide");
    $("span[id='peers-errors']").removeClass("hide");
  }
}
function Save_Settings()
{
  $("input[id^='setting-']").removeClass("input-error");
  $("input[id^='setting-']").removeClass("input-changed");
  $("div[id^='setting-']").addClass("hide");
  $("span[id='settings-errors']").addClass("hide");

  $nickname = $("input[id='setting-nickname']").val();
  $download_location = $("input[id='setting-downloadlocation']").val();
  $appip = $("input[id='setting-appip']").val();
  $appport = $("input[id='setting-appport']").val();
  $webip = $("input[id='setting-webip']").val();
  $webport = $("input[id='setting-webport']").val();
  $down = $("input[id='setting-downlimit']").val();
  $up = $("input[id='setting-uplimit']").val();
  $cert = $("input[id='setting-certlocation']").val();

  if (!nick_pattern.test($nickname)) { $("input[id='setting-nickname']").addClass("input-error"); $("div[id='setting-nickname-alert']").removeClass("hide");  }
  if (!ip_pattern.test($appip)) {  $("input[id='setting-appip']").addClass("input-error"); $("div[id='setting-appip-alert']").removeClass("hide");  }
  if (!ip_pattern.test($webip)) {  $("input[id='setting-webip']").addClass("input-error"); $("div[id='setting-webip-alert']").removeClass("hide");  }
  
  if (!port_pattern.test($appport)) { $("input[id='setting-appport']").addClass("input-error"); $("div[id='setting-appport-alert']").removeClass("hide");  }
  if (!port_pattern.test($webport)) { $("input[id='setting-webport']").addClass("input-error"); $("div[id='setting-webport-alert']").removeClass("hide");  }
  
  if (!limit_pattern.test($down)) {  $("input[id='setting-downlimit']").addClass("input-error"); $("div[id='setting-down-alert']").removeClass("hide");  }
  if (!limit_pattern.test($up)) {  $("input[id='setting-uplimit']").addClass("input-error"); $("div[id='setting-up-alert']").removeClass("hide");  }
  
  if ($("input[id^='setting-'][class~='input-error']").length ==0)
  {
    $("span[id='settings-saving']").removeClass("hide");
    var $api_action = {"action":"settingssave","data":[]};

    $api_action["data"].push(["Application IP",$appip]);
    $api_action["data"].push(["Web IP",$webip]);
    $api_action["data"].push(["Application Port",parseInt($appport)]);
    $api_action["data"].push(["Web Port",parseInt($webport)]);
    $api_action["data"].push(["Nickname",$nickname]);
    $api_action["data"].push(["Upload Limit",parseInt($up)]);
    $api_action["data"].push(["Download Limit",parseInt($down)]);
    $api_action["data"].push(["Download Location",$download_location]);
    $api_action["data"].push(["TacoNET Certificates Store",$cert]);
    $("button[id='save-settings']").prop("disabled",true);
    $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
      {
        if (data==1) {
          $("span[id='settings-unsaved']").addClass("hide");
          $("span[id='settings-saving']").addClass("hide");
          $("span[id='settings-saved']").hide().removeClass("hide").fadeIn();
          setTimeout(function()
            {
              $("span[id='settings-saved']").fadeOut(1000,function()
              {
                $("button[id='save-settings']").prop("disabled",false);
              });
            },2000);
        }
      }
    });

  }
  else
  {
    $("span[id='settings-errors']").removeClass("hide");
  }

  
}

function Confirm_Add_Peer()
{
  var $possible_json = $('#addPeerModal #ineedthis').val();
  try
  {
    var $json_data  = JSON.parse($possible_json);
    
    if ('hostname' in $json_data == false) { throw "No hostname field, your peer probably did not enter in a hostname before sending you the \"Quick Connect String\"."; }
    if ('port' in $json_data == false) { throw "No port field,your peer probably did not enter in a port before sending you the \"Quick Connect String\"."; }
    if ('serverkey' in $json_data == false) { throw "No serverkey field, your peer probably needs to regenerate his public/private keys. You should probably not be seeing this error."; }
    if ('clientkey' in $json_data == false) { throw "No clientkey field, your peer probably needs to regenerate his public/private keys. You should probably not be seeing this error."; }
    if (!port_pattern.test($json_data["port"])) { throw "Bad Port Format, your peer provided you with what appears to either be an out-of-range port, or simply not a integer."; }
    if (!z85_pattern.test($json_data["clientkey"])) { throw "Bad Clientkey Format, your peer has a bad clientkey format. You shouldn't see this error."; }
    if (!z85_pattern.test($json_data["serverkey"])) { throw "Bad Serverkey Format, your peer has a bad serverkey format. You shouldn't see this error."; }
    if (!uuid_pattern.test($json_data["uuid"])) { throw "Invalid UUID field, the UUID your peer provided doesn't appear to actually be a valid UUID."; }
    if ($json_data["uuid"] == $("#addpeermyuuid").val()) { throw "Your peer cannot have the same UUID as yourself. Don't go copying and pasting things randomly. As you see here, this won't work."; }
    if ($json_data["clientkey"] == $("#addpeermyclientpublic").val()) { throw "Cannot have a duplicate Client Key, you and your peer cannot share the same public keys."; }
    if ($json_data["serverkey"] == $("#addpeermyserverpublic").val()) { throw "Cannot have a duplicate Server Key, you and your peer cannot share the same public keys."; }

    $("div[id='addapeerbelow']").addClass("hide");
    $("div[id='peer-add-helper'] .peerblock").clone().removeAttr("id").removeClass("hide").attr("id","TEMPPEER").appendTo("div[id='peer-listing']"); 
    $("#TEMPPEER .peerhost").val($json_data["hostname"]);
    $("#TEMPPEER .peerport").val($json_data["port"]);
    $("#TEMPPEER .peerlocalnick").val("");
    $("#TEMPPEER .peeruuid").val($json_data["uuid"]);
    $("#TEMPPEER .peerclient").val($json_data["clientkey"]);
    $("#TEMPPEER .peerserver").val($json_data["serverkey"]);
    $("#TEMPPEER").removeAttr("id");
    $('#addPeerModal').modal('hide');
    $("span[id='peers-unsaved']").removeClass("hide"); 
    Set_Up_Peer_Buttons();
    
  }
  catch(err)
  {
    $("#addPeerModal #bad-connect-string").removeClass("hide").find(".exact-error").html(err);
  }

}
function Update_CopyPastePeerThing()
{
  var $jsonthing = {};
  $jsonthing["hostname"] = $("#addpeermyhostname").val();
  $jsonthing["port"] = $("#addpeermyport").val();
  $jsonthing["serverkey"] = $("#addpeermyserverpublic").val();
  $jsonthing["clientkey"] = $("#addpeermyclientpublic").val();
  $jsonthing["uuid"] = $("#addpeermyuuid").val();
  $("#peerneedsthis").html(JSON.stringify($jsonthing));

}
function Add_Peer()
{
  $('#addPeerModal button[id="addpeercancelbutton"]').unbind("click").click(function() {$('#addPeerModal').modal('hide'); } );
  $('#addPeerModal button[id="addpeerconfirmbutton"]').unbind("click").click(function() { Confirm_Add_Peer(); } );
  $('#addPeerModal #ineedthis').val("");
  $('#addPeerModal').modal();
  Update_CopyPastePeerThing();
}
function Delete_Peer($id)
{
  var $peername = $id.closest(".peerblock").find(".peernick").html() +  " @ " + $id.closest(".peerblock").find(".peerhost").val() +  ":" + $id.closest(".peerblock").find(".peerport").val();
  var $fadeoutdiv = $id.closest(".peerblock");
  $('#deletePeerModal .modal-body').html("<h5>Delete Peer: <b>"+$peername+"</b>?</h5>");
  $('#deletePeerModal').modal();
  $("button[id='deletepeerconfirmbutton']").unbind("click").click(function() { Confirm_Delete_Peer($peername,$fadeoutdiv); });

}
function Confirm_Delete_Peer($peer,$div)
{
  $('#deletePeerModal').modal('hide');
  $div.fadeOut(1000,function() { $(this).remove(); if ($("div[id='peer-listing'] .peerblock").length == 0) { $("div[id='addapeerbelow']").removeClass("hide"); } });
  $("span[id='peers-unsaved']").removeClass("hide");

}
function Set_Up_Peer_Buttons()
{
  $("button[class~='peer-enabled-button']").unbind("click").click(function() { 
      $(this).data("status",!$(this).data("status"));
      $(this).closest(".peerblock").toggleClass("green-bg").toggleClass("red-bg");
      if ($(this).find("span[class='peer-text']").html() == "Enable Peer") { $(this).find("span[class='peer-text']").html("Disable Peer");  } else { $(this).find("span[class='peer-text']").html("Enable Peer") }
      $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-stop").toggleClass("glyphicon-play");
      $("#peers-unsaved").removeClass("hide");
  });

  $("button[class~='peer-static-button']").unbind("click").click(function() {
      $(this).data("status",!$(this).data("status"));
      if ($(this).find("span[class='peer-text']").html() == "Dynamic Hostname/IP") { $(this).find("span[class='peer-text']").html("Static Hostname/IP");  } else { $(this).find("span[class='peer-text']").html("Dynamic Hostname/IP") }
      $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-random").toggleClass("glyphicon-lock");
      $("#peers-unsaved").removeClass("hide");
  });
 $(".toggle-advanced-peer-options").unbind("click").click(function() {
   $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-wrench").toggleClass("glyphicon-hand-right");
   if ($(this).find('.advanced-text').html() == "Hide Advanced Settings") { $(this).find('.advanced-text').html("Show Advanced Settings"); } else { $(this).find('.advanced-text').html("Hide Advanced Settings"); }
   $button = $(this);
   $(this).closest(".peerblock").find(".advanced-options").slideToggle();

 });
 $(".delete-peer").unbind("click").click(function() {
   Delete_Peer($(this));
   $(this).prop("disabled",false); 
 });

  $("button").popover(); 
}
function Check_For_API_Errors()
{
  var $api_action = {"action":"apistatus","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    setTimeout(Check_For_API_Errors,1000);
  }
  });
}

$( document ).ready(function() {
 Set_Up_Delete_Share();
 Set_Up_Peer_Buttons();
 Check_For_API_Errors();
 $("button[id='add-share']").click(function() { Add_Share(); });
 
 $("button[id='browsedownload']").click(function() { Download_Browse(); });
 $("button[id='browsecert']").click(function() { Cert_Browse(); });

 $("button[id='add-peer']").click(function() { Add_Peer(); });

 $("button[id='save-shares']").prop("disabled",false).click(function() { Save_Shares(); });
 $("button[id='save-settings']").prop("disabled",false).click(function() { Save_Settings(); });
 $("button[id='save-peers']").prop("disabled",false).click(function() { Save_Peers(); });

 $('#addShareModal').on('shown.bs.modal', function () {$('#addsharename').focus();  });
 $('#addPeerModal').on('shown.bs.modal', function () {$('#addpeername').focus(); $("#addPeerModal span").popover();});

 $("button[class='close']").click(function() { $(this).parent().addClass("hide");});
 $("span").popover();
 $("button").popover();

 $("input[id^='setting-']").on("change keyup paste", function(){
   $(this).addClass("input-changed");
   $("span[id='settings-unsaved']").removeClass("hide");
 });
 $(".peerblock input").on("change keyup paste", function(){
   $(this).addClass("input-changed");
   $("span[id='peers-unsaved']").removeClass("hide");
 });

 $('#addPeerModal #peerneedsthis').click(function() { $(this).select(); } );
 
 $("#addpeermyhostname").on("change keyup paste", function(){ Update_CopyPastePeerThing(); });
 $("#addpeermyport").on("change keyup paste", function(){ Update_CopyPastePeerThing(); });
 
 $("#getexternalip").click(function() {
    $button = $(this);
    $(this).prop("disabled",true).find("span[class='button-text']").html("Working...");
    $.get("/get/ip",function(data) {
      $("#addpeermyhostname").val(data); 
      Update_CopyPastePeerThing();
      $button.prop("disabled",false).find("span[class='button-text']").html("Get External IP");
    });
  }); 

});

