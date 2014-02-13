var $stage=1;
var $failcount = 0;
function Get_Share_Listing_Results(browse_uuid)
{
  console.log("Get_Share_Listing_Results:" + browse_uuid);
  $failcount++;
  if ($failcount > 30) 
  {
     $("#loaderthing").addClass("hide");
     $("#timedout").fadeIn();
  }
  else
  {
    setTimeout(function() { Get_Share_Listing_Results(browse_uuid) },100);
  }

}
function Show_Peer_Shares(nickname,localnick,peer_uuid)
{
  $stage=2;
  console.log("Show_Peer_Shares: " + peer_uuid);
  $crumbs = [];
  $crumbs.push('<li><a href="/browse.taco">Peer Listing</a></li>');
  if (localnick != "") {
    $crumbs.push('<li>'+nickname+' ('+localnick+')</li>');
  } else {
    $crumbs.push('<li>'+nickname+'</li>');
  }
  $("#peercrumb").html('<ol class="breadcrumb">'+$crumbs.join("")+'</ol>');
  $("#peerlisting").addClass("hide");
  $("#loaderthing").removeClass("hide");
  $("#peercrumb").slideDown();

  var $api_action = {"action":"browse","data":{"uuid":peer_uuid,"share":"/","dir":"/"}};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
    {
      setTimeout(function() { Get_Share_Listing_Results(data["result"]) },100);
    }
  });
}
function Set_Up_Root_Peer_Names()
{
  if ($stage != 1) { return; }
  console.log("Set_Up_Root_Peer_Names");
  var $api_action = {"action":"peerstatus","data":""};

  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
    {
      listing = [];
      for (var $uuid in data) 
      {
          inc = data[$uuid][0];
          out = data[$uuid][1];
          indiff = data[$uuid][2];
          outdiff = data[$uuid][3];
          nick = data[$uuid][4];
          localnick = data[$uuid][5];
          if (indiff < 6.0 && indiff >= 0.0 && outdiff < 6.0 && outdiff >= 0.0)
          {
            thestring = '<a data-uuid="'+$uuid+'" class="peerclick list-group-item" href="#"><span class="glyphicon glyphicon-user"></span> <strong>'+nick+'</strong>';
            if (localnick != "") { thestring += ' ('+localnick+')'; }
            thestring += "</a>";
            listing.push(thestring);
          }
      }
      
      if (listing.length > 0)
      {
        $("#loaderthing").addClass("hide");
        $("#nopeers").fadeOut(function() 
        {
          if ($("#peerlisting").html() != listing.join("")) 
          { 
            $("#peerlisting").fadeOut(function() 
            { 
              $(this).html(listing.join(""));
              $(".peerclick").unbind("click").click(function()
              {
                Show_Peer_Shares(nick,localnick,$(this).data("uuid"));
              });
              $(this).fadeIn(function() { setTimeout(Set_Up_Root_Peer_Names,1000) });
            });
          }
          else
          {
            setTimeout(Set_Up_Root_Peer_Names,1000);
          }
        });
      }
      else
      {
        $("#loaderthing").addClass("hide");
        $("#peerlisting").fadeOut(function() { $fadedef = $("#nopeers").fadeIn(function() { setTimeout(Set_Up_Root_Peer_Names,1000) }) });
      }

    }
  });

}


$( document ).ready(function() {
  Set_Up_Root_Peer_Names();

});
