function Update_Download_Q()
{
  var $api_action = {"action":"downloadqget","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    if ("result" in data && "peerinfo" in data)
    {
      table=[];
      for (peer_uuid in data["result"])
      {
        console.log(peer_uuid);console.log(data["result"][peer_uuid]);console.log(data["peerinfo"]);
        if (data["peerinfo"][peer_uuid][1] != "")
        {
          table.push("<h4>"+data["peerinfo"][peer_uuid][0] + " <small>(" + data["peerinfo"][peer_uuid][1] + ")</small></h4>");
        }else {
          table.push("<h4>"+data["peerinfo"][peer_uuid][0]+"</h4>");
        }
        table.push("<table class='table table-striped table-hover table-condensed table-bordered'>");
        table.push("<tbody>");
        for (var i = 0; i < data["result"][peer_uuid].length; i++) 
        {
          table.push("<tr>");
          table.push("<td><big>" + data["result"][peer_uuid][i][1] + "</big> ("+commify(data["result"][peer_uuid][i][2])+" bytes)<br>" + data["result"][peer_uuid][i][0] + "</td>");
          table.push('<td style="width: 30%; vertical-align: middle;" class="text-center"><div style="margin-bottom: 0px" class="progress"><div class="progress-bar" role="progressbar" style="width: 5%;"></div></div>Data here</td>');
          table.push("</tr>");
          console.log(data["result"][peer_uuid][i]);
        }
        table.push("</tbody></table>");
      }
      $("#downloadqdiv").html(table.join(""));
    }
  }});

}

$( document ).ready(function() {
  Check_For_API_Errors();
  Update_Download_Q();
});
