function Set_Up_Root_Peer_Names()
{
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
            thestring = '<a data-uuid="'+$uuid+'"class="peerclick list-group-item" href="#"><span class="glyphicon glyphicon-user"></span> <strong>'+nick+'</strong>';
            if (localnick != "") { thestring += ' ('+localnick+')'; }
            thestring += "</a>";
            listing.push(thestring);
          }
      }
      console.log(listing);
      if (listing.length > 0)
      {
        $("#nopeers").fadeOut(function() {
          $("#filelisting").html(listing.join(""));
        });
      }
      else
      {
        $("#nopeers").fadeIn(function() {
          setTimeout(Set_Up_Root_Peer_Names,1000);
        });
      }

    }
  });

}


$( document ).ready(function() {
  Set_Up_Root_Peer_Names();

});
