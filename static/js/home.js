function Update_Peer_Status()
{
    var $api_action = {"action":"peerstatus","data":""};
    
    $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
      {
        //console.log(data);
        $("#peerstatustable .loadingthing").addClass("hide");
        $uuids_that_exists = [];

        //slideout disabled peers
        $(".peerstatusrow").each(function() 
        {
          if ($(this).attr("id") in data) 
          {
          } else { 
            $(this).slideUp(function() { $(this).remove(); });
          }
        });

        for (var $uuid in data)
        {
          inc = data[$uuid][0];
          out = data[$uuid][1];
          indiff = data[$uuid][2];
          outdiff = data[$uuid][3];
          nick = data[$uuid][4];
          localnick = data[$uuid][5];
          if (indiff  < 10000000) { $inmsg = indiff.toFixed(2) + " second(s) ago" } else { $inmsg = "Never" }
          if (outdiff < 10000000) { $outmsg = outdiff.toFixed(2) + " second(s) ago" } else { $outmsg = "Never" }
          if (localnick != "") { $localnickmsg = "<br>(" + localnick + ")" } else { $localnickmsg = "" }
          if ($("#" + $uuid).length == 1) 
          { 
            $tr = $("#" + $uuid); 
            if ($tr.find(".tablenick").html() != nick) { $tr.find(".tablenick").html(nick); }
            if ($tr.find(".localnick").html() != $localnickmsg) { $tr.find(".localnick").html($localnickmsg); }
            if ($tr.find(".lastincoming").html() != $inmsg) { $tr.find(".lastincoming").html($inmsg); }
            if ($tr.find(".lastoutgoing").html() != $outmsg) { $tr.find(".lastoutgoing").html($outmsg); }
          } else {
            $tr = $("#peerstatusrowhelper");
            $tr.clone().removeClass("hide").addClass("peerstatusrow").removeAttr("id").attr("id",$uuid).appendTo("#peerstatustbody");
            $tr = $("#" + $uuid);
            if ($tr.find(".tablenick").html() != nick) { $tr.find(".tablenick").html(nick); }
            if ($tr.find(".localnick").html() != $localnickmsg) { $tr.find(".localnick").html($localnickmsg); }
            if ($tr.find(".lastincoming").html() != $inmsg) { $tr.find(".lastincoming").html($inmsg); }
            if ($tr.find(".lastoutgoing").html() != $outmsg) { $tr.find(".lastoutgoing").html($outmsg); }

          }
          if (indiff >= 6.0) 
          { 
            $tr.find(".incomingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-ok-sign").addClass("glyphicon-minus-sign"); 
            $tr.find(".incomingstatus").removeClass("yellow-td green-td").addClass("red-td");
          }
          else if (indiff < 6.0 && indiff >= 0.0) 
          {
            $tr.find(".incomingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-minus-sign").addClass("glyphicon-ok-sign");
            $tr.find(".incomingstatus").removeClass("yellow-td red-td").addClass("green-td");
          }

          if (outdiff >= 6.0)
          {
            $tr.find(".outgoingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-ok-sign").addClass("glyphicon-minus-sign");
            $tr.find(".outgoingstatus").removeClass("yellow-td green-td").addClass("red-td");
          }
          else if (outdiff < 6.0 && outdiff >= 0.0)
          {
            $tr.find(".outgoingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-minus-sign").addClass("glyphicon-ok-sign");
            $tr.find(".outgoingstatus").removeClass("yellow-td red-td").addClass("green-td");
          }
        }
        setTimeout(Update_Peer_Status,500 + (Math.random()*500)+1);
      }
    });

}
function Update_Thread_Status()
{
    var $api_action = {"action":"threadstatus","data":""};

    $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
      {
        if ("threads" in data) {
          if ("clients" in data["threads"])
          {
            if ("alive" in data["threads"]["clients"]) { if (data["threads"]["clients"]["alive"]) { $("#clientalive").html("Running"); } else {$("#clientalive").html("Stopped");}   }
            if ("status" in data["threads"]["clients"]) { $("#clientstatus").html(data["threads"]["clients"]["status"]); }
            if ("lastupdate" in data["threads"]["clients"]) { $("#clientlast").html(data["threads"]["clients"]["lastupdate"].toFixed(2) + " second(s) ago"); }
          }
          if ("server" in data["threads"])
          {
            if ("alive" in data["threads"]["server"]) { if (data["threads"]["server"]["alive"]) { $("#serveralive").html("Running"); } else {$("#serveralive").html("Stopped");}   }
            if ("status" in data["threads"]["server"]) { $("#serverstatus").html(data["threads"]["server"]["status"]); }
            if ("lastupdate" in data["threads"]["server"]) { $("#serverlast").html(data["threads"]["server"]["lastupdate"].toFixed(2) + " second(s) ago"); }
          }

     
        }
        setTimeout(Update_Thread_Status,1500 + (Math.random()*500)+1);
      }
    });
}

$( document ).ready(function() {
  Update_Peer_Status();
  Update_Thread_Status();
  Check_For_API_Errors();
});

