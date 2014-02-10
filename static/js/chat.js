function Update_Chat_Log()
{
  $("#ajaxloader").removeClass('hide');
  var $api_action = {"action":"getchat","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
  {
    $("#chatlog").html("");
    for (var i = 0; i < data.length; i++) 
    {
      if (data[i][0] == 0)
      {
        var newDate = new Date();
        newDate.setTime(data[i][3]*1000);
        dateString = newDate.toString();
        $(".panel-body .local-helper").clone().removeClass("local-helper").attr("id","chathelper").removeClass("hide").appendTo("#chatlog");
        $("#chathelper .nick").html(data[i][1]);
        $("#chathelper .themsg").html(data[i][4]);
        $("#chathelper .thetime").html(dateString);
        $("#chathelper").removeAttr("id");
      }
      else
      {
        var newDate = new Date();
        newDate.setTime(data[i][3]*1000);
        dateString = newDate.toString();
        $(".panel-body .remote-helper").clone().removeClass("remote-helper").attr("id","chathelper").removeClass("hide").appendTo("#chatlog");
        $("#chathelper .nick").html(data[i][1]);
        $("#chathelper .themsg").html(data[i][4]);
        $("#chathelper .thetime").html(dateString);
        $("#chathelper").removeAttr("id");

      }
    }
    $("#ajaxloader").addClass('hide');
    $("#chatlog").scrollTop($("#chatlog").prop("scrollHeight"));
  }
  });


}
function Send_Chat_Msg(msg)
{
  var $api_action = {"action":"sendchat","data":msg};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
  {
    if (data==1)
    {
      Update_Chat_Log();
    }
  }
  });


}
function Update_On_Change()
{
  console.log("Update On Change");
  var $api_action = {"action":"chatuuid","data":""};
  $something = $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
  {
    if (data[0] != $("#chatbox").data("uuid")) { $("#chatbox").data("uuid",data); Update_Chat_Log(); }
    setTimeout(function() { Update_On_Change(); },1000);
  }});
  console.log($something);
}
$( document ).ready(function() {
  $('#chatbox').focus().keypress(function(e) {
      if (e.which == 13) {
        Send_Chat_Msg($('#chatbox').val());
        $('#chatbox').val("");
        $('#chatbox').focus();
        return false;    //<---- Add this line
      }
    });
  $("#chatbutton").click(function(){
    Send_Chat_Msg($('#chatbox').val());
    $('#chatbox').val("");
    $('#chatbox').focus();
  });
  Update_Chat_Log();
  $("#chatbox").data("uuid",guid());
  setTimeout(function() { Update_On_Change(); } , 1000);
});

