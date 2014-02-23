var $stage=1;
var $failcount = 0;
function Get_Share_Listing_Results(peer_uuid,sharedir)
{
  console.log("Get_Share_Listing_Results: " + sharedir);
  $("#sharelisting").html("");
  $("#loaderthing").removeClass("hide");
  if ($failcount > 200) 
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
            thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+btoa(updirstr)+'" class="shareclick list-group-item">';
            thestring += '<span class="glyphicon glyphicon-arrow-left"></span> <strong>.. [BACK]</strong>';
            thestring += '</li>';
            sharelisting.push(thestring);
          }

          for (var i = 0; i < data["result"][1].length; i++) 
          {
            if (sharedir=="/") { 
              thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+btoa(sharedir+data["result"][1][i])+'" class="shareclick list-group-item">';
              thestring += '<span class="glyphicon glyphicon-bookmark"></span> <strong>'+data["result"][1][i]+'</strong>';
            }
            else {
              thestring = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+btoa(sharedir+"/"+data["result"][1][i])+'" class="shareclick list-group-item">';
              thestring += '<span class="sharelistingbuttonblock"><div class="btn-group btn-group-xs">';
              thestring += '<button type="button" class="btn btn-default diraddtoq"><span class="glyphicon glyphicon-plus"></span></button>';
              thestring += '<button type="button" class="btn btn-default dirsubscribe"><span class="glyphicon glyphicon-tag"></span></button>';
              thestring += '</div></span>';
              thestring += '<span class="glyphicon glyphicon-folder-open"></span> <strong>'+data["result"][1][i]+'</strong>';
            }
            thestring += '</li>';
            sharelisting.push(thestring);
          }
          filelisting = [];
          for (var i = 0; i < data["result"][2].length; i++)
          {
            thestring  = '<li data-uuid="'+peer_uuid+'" data-sharedir="'+btoa(sharedir)+'" data-filename="'+btoa(data["result"][2][i][0])+'" data-size="'+data["result"][2][i][1]+'" data-mod="'+data["result"][2][i][2]+'" class="fileclick list-group-item">';
            thestring += '<span class="sharelistingbuttonblock"><div class="btn-group btn-group-xs">';
            thestring += '<button type="button" class="btn btn-default fileaddtoq"><span class="glyphicon glyphicon-plus"></span></button>';
            thestring += '</div></span>';
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
                  l_sharedir = atob($(this).data("sharedir"));
                  var $api_action = {"action":"browse","data":{"uuid":$(this).data("uuid"),"sharedir":atob($(this).data("sharedir"))}};
                  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
                    {
                      Get_Share_Listing_Results(l_uuid,l_sharedir);
                    }
                  });
                });
                $(".fileaddtoq").unbind("click").click(function(event) 
                {
                  event.stopPropagation();
                  filename=$(this).closest(".fileclick").data("filename");
                  path=$(this).closest(".fileclick").data("sharedir");
                  peer_uuid=$(this).closest(".fileclick").data("uuid");
                  modtime=$(this).closest(".fileclick").data("mod");
                  size=$(this).closest(".fileclick").data("size");
                  $(this).find("span").toggleClass("glyphicon-refresh glyphicon-plus spinner");
                  buttonthis = $(this);
                  var $api_action = {"action":"downloadqadd","data":{"uuid":peer_uuid,"sharedir":atob(path),"filename":atob(filename),"filesize":size,"filemodtime":modtime}};
                  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
                  {
                    if (data == 1) { buttonthis.find("span").toggleClass("spinner glyphicon-refresh glyphicon-ok"); buttonthis.unbind("click"); buttonthis.toggleClass("btn-success"); }
                    else if (data == 2) { buttonthis.find("span").toggleClass("spinner glyphicon-refresh glyphicon-ok"); buttonthis.unbind("click"); buttonthis.toggleClass("btn-info"); }
                    else { buttonthis.find("span").toggleClass("spinner glyphicon-refresh glyphicon-remove"); buttonthis.unbind("click"); buttonthis.toggleClass("btn-danger"); }
                  }});
  
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
  $crumbs.push('<li><a href="/browse.taco">Return to Peer Listing</a></li>');
  if (localnick != "") {
    $crumbs.push('<li><a id="peerrootcrumb" href="#">'+nickname+' ('+localnick+') Share Listing</a></li>');
  } else {
    $crumbs.push('<li><a id="peerrootcrumb" href="#">'+nickname+' Share Listing</a></li>');
  }
  $("#peercrumb").html('<ol class="breadcrumb">'+$crumbs.join("")+'</ol>');
  $("#peerlisting").addClass("hide");
  $("#sharelisting").removeClass("hide");
  $("#loaderthing").removeClass("hide");
  $("#peercrumb").slideDown(150);
  $("#peerrootcrumb").unbind("click").click(function () 
  {
    $("#sharelisting").fadeOut(200,function() {
    Show_Peer_Shares(nickname,localnick,peer_uuid);
    });
  });
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
