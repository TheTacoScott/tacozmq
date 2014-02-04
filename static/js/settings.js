//SHARES
//Delete Function
function Setup_Share_Delete_Buttons()
{
 $("div[id='share-listing'] button[data-type='share'][data-action='delete']").click(function()
 {
    var $index = $(this).data("index");
    var $fadeoutdiv = $(this).parent().parent();
    //if (confirm('Are you sure you want to delete this share?')) {
    //  $.get('/sharedelete/' + $index, function(data){
    //    if (data=="1") { $fadeoutdiv.fadeOut(1000,function() { $(this).remove();}); }
    //  });
    //}
     $('#deleteShareModal .modal-body').html("<h5>Delete sharename: <b>"+$(this).data("name")+"</b>?</h5>");
     $('#deleteShareModal').modal();
  

  });

}
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
  });
}
function Share_Browse_Setup()
{
  $("#sharebrowselistdiv a[class='list-group-item']").click(function()
  {
    $browsedir = $(this).data("browsedir");
    Share_Browse($browsedir);
  });
}
function Confirm_Add_Share()
{
  $("#addShareModal .modal-body div[id='alphanumonly']").removeClass('hide');
  setTimeout(function() { $("#addShareModal .modal-body div[id='alphanumonly']").fadeOut(); },5000);  
}
function Add_Share()
{
  //$("div[id='share-add-helper']").clone().removeAttr("id").removeClass("hide").appendTo("div[id='share-listing']");
  Share_Browse();
  $("#addshareloc").val("/");
  $("#addsharename").val("");
  $('#addShareModal').modal();
  

}

function Save_Shares()
{

  $("button[id='save-shares']").prop("disabled",true);
  $("span[id='shares-saving']").removeClass("hide");
  var deferreds = [];
  $("div[id='share-listing'] div[class='input-group']").each(function()
  {
    var $sharename = $(this).find("span:first").html();
    var $text = $(this).find("input[type='text']").val();
    var $placeholder = $(this).find("input[type='text']").attr("placeholder");
    var $index = $(this).find("button:first").data("index")
    if ($text == "") { $text = $placeholder; }
    if ($text != "") {
      deferreds.push($.get('/shareedit/' + $index + "/" + $sharename + "/" + $text,function(data)
      {
        var waiting=1;   
      }));
    }
  });
  
  $.when.apply($,deferreds).then(function() {
    setTimeout(function() {
    $("span[id='shares-saving']").addClass("hide");
    $("span[id='shares-saved']").hide().removeClass("hide").fadeIn();
    setTimeout(function() { $("span[id='shares-saved']").fadeOut(1000,function() {$("button[id='save-shares']").prop("disabled",false);});},2000);
    },500);
  });
}

$( document ).ready(function() {
 Setup_Share_Delete_Buttons();
 $("button[id='add-share']").click(function() { Add_Share(); });
 $("button[id='save-shares']").click(function() { Save_Shares(); });
 $("button[id='addsharecancelbutton']").click(function() { $("#sharebrowselistdiv").scrollTop(0); $('#addShareModal').modal('hide');  });
 $("button[id='addshareconfirmbutton']").click(function() { Confirm_Add_Share(); });

 $('#addShareModal').on('shown.bs.modal', function () {
    $('#addsharename').focus();
 });


});

