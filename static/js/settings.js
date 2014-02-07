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
  $sharename = $("input[id='addsharename']").val();
  $sharelocation = $("input[id='addshareloc']").val();
  if (pattern.test($sharename))
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




$( document ).ready(function() {
 Set_Up_Delete_Share();
 $("button[id='add-share']").click(function() { Add_Share(); });
 $("button[id='save-shares']").prop("disabled",false).click(function() { Save_Shares(); });

 $('#addShareModal').on('shown.bs.modal', function () {$('#addsharename').focus();  });
 $("button[class='close']").click(function() { $(this).parent().addClass("hide");});

});

