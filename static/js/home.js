function Update_Peer_Status()
{
  $(".peerstatusrow").each(function() {
    $uuid = $(this).data("uuid");
    var $api_action = {"action":"peerstatus","data":$uuid};
    var $tr = $(this);
    $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",success: function(data)
      {
        console.log(data);
        inc = data[0];
        out = data[1];
        indiff = data[2];
        outdiff = data[3];
        if (indiff >= 5.0) 
        { 
          $tr.find(".incomingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-ok-sign").addClass("glyphicon-minus-sign"); 
          $tr.find(".incomingstatus").removeClass("yellow-td green-td").addClass("red-td");
        }
        else if (indiff < 5.0 && indiff >= 0.0) 
        {
          $tr.find(".incomingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-minus-sign").addClass("glyphicon-ok-sign");
          $tr.find(".incomingstatus").removeClass("yellow-td red-td").addClass("green-td");
        }

        if (outdiff >= 5.0)
        {
          $tr.find(".outgoingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-ok-sign").addClass("glyphicon-minus-sign");
          $tr.find(".outgoingstatus").removeClass("yellow-td green-td").addClass("red-td");
        }
        else if (outdiff < 5.0 && outdiff >= 0.0)
        {
          $tr.find(".outgoingstatus").find(".glyphicon").removeClass("glyphicon-question-sign glyphicon-minus-sign").addClass("glyphicon-ok-sign");
          $tr.find(".outgoingstatus").removeClass("yellow-td red-td").addClass("green-td");
        }

      }
    });

  });
}


$( document ).ready(function() {
  $("span").popover();
  Update_Peer_Status();
});

