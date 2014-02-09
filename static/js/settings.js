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
  $.ajax({url:"/api/share",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
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

function Save_Settings()
{
  var nick_pattern = new RegExp("^[a-zA-Z0-9\. ]{3,64}$");
  var ip_pattern = new RegExp("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
  var port_pattern = new RegExp("^0*(?:6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|[0-9])$");
  var limit_pattern = new RegExp("^[1-9][0-9]+$");

  $("input[id^='setting-']").removeClass("input-error");
  $("input[id^='setting-']").removeClass("input-changed");
  $("div[id^='setting-']").addClass("hide");

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
    $.ajax({url:"/api/settings",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
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

  
}

function Confirm_Add_Peer()
{
  var $possible_json = $('#addPeerModal #ineedthis').val();
  try
  {
    var $json_data  = JSON.parse($possible_json);
    if(!'hostname' in $json_data) { throw "No hostname field"; }
  }
  catch(err)
  {
    $("#addPeerModal #bad-connect-string").removeClass("hide");
  }

}
function Update_CopyPastePeerThing()
{
  var $jsonthing = {};
  $jsonthing["hostname"] = $("#addpeermyhostname").val();
  $jsonthing["port"] = $("#addpeermyport").val();
  $jsonthing["serverkey"] = $("#addpeermyclientpublic").val();
  $jsonthing["clientkey"] = $("#addpeermyserverpublic").val();
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

function Set_Up_Peer_Buttons()
{
  $("button[class~='peer-enabled-button']").unbind("click").click(function() { 
    $(this).toggleClass("btn-success").toggleClass("btn-danger"); 
      $(this).data("status",!$(this).data("status"));
      if ($(this).find("span[class='peer-text']").html() == "Peer Enabled") { $(this).find("span[class='peer-text']").html("Peer Disabled");  } else { $(this).find("span[class='peer-text']").html("Peer Enabled") }
      $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-stop").toggleClass("glyphicon-play");
      $("#peers-unsaved").removeClass("hide");
  });

  $("button[class~='peer-static-button']").unbind("click").click(function() {
    $(this).toggleClass("btn-info").toggleClass("btn-warning");
      $(this).data("status",!$(this).data("status"));
      if ($(this).find("span[class='peer-text']").html() == "Dynamic Hostname/IP") { $(this).find("span[class='peer-text']").html("Static Hostname/IP");  } else { $(this).find("span[class='peer-text']").html("Dynamic Hostname/IP") }
      $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-random").toggleClass("glyphicon-lock");
      $("#peers-unsaved").removeClass("hide");
  });
 $(".toggle-advanced-peer-options").unbind("click").click(function() {
   $(this).find("span[class~='glyphicon']").toggleClass("glyphicon-wrench").toggleClass("glyphicon-hand-right");
   if ($(this).find('.advanced-text').html() == "Hide Advanced Settings") { $(this).find('.advanced-text').html("Show Advanced Settings"); } else { $(this).find('.advanced-text').html("Hide Advanced Settings"); }
   $button = $(this);
   $(this).parent().parent().find(".advanced-options").slideToggle();

 });

  $("button").popover(); 
}

$( document ).ready(function() {
 Set_Up_Delete_Share();
 Set_Up_Peer_Buttons()
 $("button[id='add-share']").click(function() { Add_Share(); });
 
 $("button[id='browsedownload']").click(function() { Download_Browse(); });
 $("button[id='browsecert']").click(function() { Cert_Browse(); });

 $("button[id='add-peer']").click(function() { Add_Peer(); });
 $("button[id='save-shares']").prop("disabled",false).click(function() { Save_Shares(); });
 $("button[id='save-settings']").prop("disabled",false).click(function() { Save_Settings(); });

 $('#addShareModal').on('shown.bs.modal', function () {$('#addsharename').focus();  });
 $('#addPeerModal').on('shown.bs.modal', function () {$('#addpeername').focus();  });

 $("button[class='close']").click(function() { $(this).parent().addClass("hide");});
 $("span").popover();
 $("button").popover();

 $("input[id^='setting-']").on("change keyup paste", function(){
   $(this).addClass("input-changed");
   $("span[id='settings-unsaved']").removeClass("hide");
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

