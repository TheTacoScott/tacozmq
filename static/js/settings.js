//SHARES
//Delete Function
function Setup_Share_Delete_Buttons()
{
 $("div[id='share-listing'] button[data-type='share'][data-action='delete']").click(function()
 {
    var $index = $(this).data("index");
    var $fadeoutdiv = $(this).parent().parent();
    if (confirm('Are you sure you want to delete this share?')) {
      $.get('/sharedelete/' + $index, function(data){
        if (data=="1") { $fadeoutdiv.fadeOut(1000,function() { $(this).remove();}); }
      });
    }

  });

}
function Setup_Share_Rename_Buttons()
{
 $("div[id='share-listing'] button[data-type='share'][data-action='rename']").click(function()
 {
    var $newname = prompt("What do you want to call this share?",$(this).data("name"));
    if ($newname != null) { $(this).data("name",$newname); $(this).find("span[class='sharenamedisplay']").html($newname); }
 });

}

function Index_Share_Buttons()
{
 $("div[id='share-listing'] button[data-type='share']").each(function()
 {
   var $index = $(this).data("index");
   if ($index == -1) { $(this).data("index",guid()); }
 });
}

function Add_Share()
{
  $("div[id='share-add-helper']").clone().removeAttr("id").removeClass("hide").appendTo("div[id='share-listing']");
  Index_Share_Buttons();
  Setup_Share_Delete_Buttons();
  Setup_Share_Rename_Buttons();
}

function Save_Shares()
{

  $("button[id='save-shares']").prop("disabled",true);
  $("span[id='shares-saving']").removeClass("hide");
  var deferreds = [];
  $("div[id='share-listing'] div[class='input-group']").each(function()
  {
    var $sharename = $(this).find("button:first").data("name");
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
 Setup_Share_Rename_Buttons();
 $("button[id='add-share']").click(function() { Add_Share(); });
 $("button[id='save-shares']").click(function() { Save_Shares(); });


});

