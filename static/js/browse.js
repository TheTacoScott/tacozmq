var $stage=1;
var $failcount = 0;
function Get_Share_Listing_Results(peer_uuid,sharedir)
{
  console.log("Get_Share_Listing_Results: " + sharedir);
  $("#sharelisting").html("");
  $("#loaderthing").removeClass("hide");
  if ($failcount > 10) 
  {
     $("#loaderthing").addClass("hide");
     $("#timedout").fadeIn();
  }
  else
  {
    var $api_action = {"action":"browseresult","data":{"uuid":peer_uuid,"sharedir":sharedir}};
    $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
      {
        if ("result" in data) 
        { 
          $("#loaderthing").addClass("hide");
          sharelisting = [];
          if (sharedir.length > 1) 
          {
            updir = sharedir.split('/');
            updir.pop();
            updirstr = updir.join('/');
            if (updirstr == "") { updirstr = "/"; }
            thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+updirstr+'" class="shareclick list-group-item">';
            thestring += '<span class="glyphicon glyphicon-arrow-left"></span> <strong>.. [BACK]</strong>';
            thestring += '</li>';
            sharelisting.push(thestring);
          }

          for (var i = 0; i < data["result"][1].length; i++) 
          {
            if (sharedir=="/") { 
              thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+sharedir+data["result"][1][i]+'" class="shareclick list-group-item">';
              thestring += '<span class="glyphicon glyphicon-bookmark"></span> <strong>'+data["result"][1][i]+'</strong>';
            }
            else {
              thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+sharedir+"/"+data["result"][1][i]+'" class="shareclick list-group-item">';
              thestring += '<span class="glyphicon glyphicon-folder-open"></span> <strong>'+data["result"][1][i]+'</strong>';
            }
            thestring += '</li>';
            sharelisting.push(thestring);
          }
          filelisting = [];
          for (var i = 0; i < data["result"][2].length; i++)
          {
            thestring  = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+sharedir+'" data-filename="" class="fileclick list-group-item">';
            thestring += '<span class="glyphicon glyphicon-file"></span> <strong>'+data["result"][2][i][0]+'</strong> <span style="float:right">'+commify(data["result"][2][i][1])+' bytes</span>';
            thestring += '</li>';
            sharelisting.push(thestring);
          } 

          
          $outputhtml  = '';
          $outputhtml += '<ul class="list-group">';
          $outputhtml += sharelisting.join("");
          $outputhtml += filelisting.join("");
          $outputhtml += '</ul>';
          if (sharelisting.length > 0)
          {
            if ($("#sharelisting").html() != $outputhtml)
            {
              $("#sharelisting").fadeOut(function()
              {
                $(this).html($outputhtml);
                $failcount = 0;
                $(".shareclick").unbind("click").click(function() 
                { 
                  l_uuid = $(this).data("uuid");
                  l_sharedir = $(this).data("sharedir");
                  var $api_action = {"action":"browse","data":{"uuid":$(this).data("uuid"),"sharedir":$(this).data("sharedir")}};
                  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
                    {
                      Get_Share_Listing_Results(l_uuid,l_sharedir);
                    }
                  });
                });
                $(this).fadeIn();
              });
            }
          }
          else
          {
            $("#noshares").fadeIn();
          }

        } 
        else 
        { 
          $failcount++; 
          setTimeout(function() { Get_Share_Listing_Results(peer_uuid,sharedir) },100);
        }
      }
    });
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
  $("#peercrumb").slideDown(150);
  var $api_action = {"action":"browse","data":{"uuid":peer_uuid,"sharedir":"/"}};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
    {
      setTimeout(function() { Get_Share_Listing_Results(peer_uuid,data["sharedir"]) },100);
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
            thestring = '<li data-nick="'+nick+'" data-localnick="'+localnick+'" data-uuid="'+$uuid+'" class="peerclick list-group-item">';
            thestring += '<span class="glyphicon glyphicon-user"></span> <strong>'+nick+'</strong>';
            if (localnick != "") { thestring += ' ('+localnick+')'; }
            thestring += '</li>';
            listing.push(thestring);
          }
      }
     
      
      if (listing.length > 0)
      {
        $("#loaderthing").addClass("hide");
        $("#nopeers").fadeOut(function() 
        {
          $outputhtml  = '';
          $outputhtml += '<ul class="list-group">';
          $outputhtml += listing.join("");
          $outputhtml += '</ul>';
          
          if ($("#peerlisting").html() != $outputhtml) 
          { 
            $("#peerlisting").fadeOut(function() 
            {
              $(this).html($outputhtml);
              //$(".peerclick button .glyphicon-download").parent().unbind("click").click(function(event) { event.stopPropagation(); });
              //$(".peerclick button .glyphicon-bookmark").parent().unbind("click").click(function(event) { event.stopPropagation(); });
              $(".peerclick").unbind("click").click(function()
              {
                Show_Peer_Shares($(this).data("nick"),$(this).data("localnick"),$(this).data("uuid"));
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
  Check_For_API_Errors();
  
});
