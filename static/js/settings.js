function Share_Browse($browsedir="")
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
    $("#sharebrowselistdiv").html(items.join(""));
    if ($browsedir=="") { $browsedir = "/"; }
    $("#addshareloc").val($browsedir);
    Share_Browse_Setup();
    $("#sharebrowselistdiv").scrollTop(0);
  });
}
function Share_Browse_Setup()
{
  $("#sharebrowselistdiv a[class='list-group-item']").unbind("click").click(function()
  {
    $browsedir = $(this).data("browsedir");
    Share_Browse($browsedir);
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
  Share_Browse();
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

$( document ).ready(function() {
 Set_Up_Delete_Share();
 $("button[id='add-share']").click(function() { Add_Share(); });
 $("button[id='save-shares']").prop("disabled",false).click(function() { Save_Shares(); });
 $("button[id='save-settings']").prop("disabled",false).click(function() { Save_Settings(); });

 $('#addShareModal').on('shown.bs.modal', function () {$('#addsharename').focus();  });
 $("button[class='close']").click(function() { $(this).parent().addClass("hide");});
 $("span").popover();

 $("input[id^='setting-']").on("change keyup paste", function(){
    $(this).addClass("input-changed");
    $("span[id='settings-unsaved']").removeClass("hide");
  })

});

