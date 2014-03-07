var $dontrefresh = false;
var $helperdontrefresh = false;

//http://stackoverflow.com/questions/1307705/jquery-ui-sortable-with-table-and-tr-width
trhelper = function(e, tr)
{
  var $originals = tr.children();
  var $helper = tr.clone();
  $helper.children().each(function(index)
  {
    $(this).width($originals.eq(index).width());
  });
  return $helper;
}

starthelper = function(event,ui)
{
  var startpos = ui.item.index();
  ui.item.data("startpos",startpos);
  $helperdontrefresh = true;
}

updatehelper = function(event,ui)
{
  console.log(ui.item.data("startpos"),ui.item.index());

  peer_uuid = ui.item.data("peeruuid");
  modtime   = ui.item.data("modtime");
  filesize  = ui.item.data("size");
  filename  = atob(ui.item.data("filename"));
  sharedir  = atob(ui.item.data("sharedir"));

  var $api_action = {"action":"downloadqmove","data":{"uuid":peer_uuid,"sharedir":sharedir,"filename":filename,"filesize":filesize,"filemodtime":modtime,"newloc":ui.item.index()}};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    console.log(data);
    $helperdontrefresh = false;
  }});

}
function Update_Completed_Q()
{
  var $api_action = {"action":"completedqget","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    if (data["result"].length == 0) { $("#completedqempty").removeClass("hide"); $("#completedfooter").addClass("hide");} 
    else 
    { 
      $("#completedqempty").addClass("hide");
      $("#completedfooter").removeClass("hide");
      $("#completedfooterremovebutton").unbind("click").click(function()
      {
          $("#completedremovebutton").unbind("click").click(function() {
            $('#removeCompletedModal').modal('hide');
            var $api_action = {"action":"completedqclear","data":{}};
            $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
            {
              if (data == 1) { location.reload(); }
            }});
        });
        $("#removeCompletedModal").modal();
      });
      table=[];
      table.push("<table class='table table-hover table-condensed table-bordered'>");
      table.push("<tbody>");
      
      for (var i = 0; i < data["result"].length; i++)
      {
        table.push("<tr><td>" + data["result"][i][0] + "</td><td>" + data["peerinfo"][data["result"][i][1]][0] + "</td><td>" + data["result"][i][2] + "</td><td class='text-left'>" + data["result"][i][3] + "</td><td>" + commify(data["result"][i][4]) + " bytes</td></tr>");
      }
      table.push("</tbody></table>");
      $("#completedqdiv").html(table.join(""));
    }
    setTimeout(Update_Completed_Q,1500);
  }});

}

function Update_Download_Q()
{
  if ($dontrefresh) { setTimeout(Update_Download_Q,1000); return; }
  console.log("1");
  var $api_action = {"action":"downloadqget","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    if ("result" in data && "peerinfo" in data && "fileinfo" in data)
    {
      $("#downloadqempty").addClass("hide");
      table=[];
      $rows_added = 0;
      for (peer_uuid in data["result"])
      {
        //console.log(peer_uuid);console.log(data["result"][peer_uuid]);console.log(data["peerinfo"]);
        if (data["peerinfo"][peer_uuid][1] != "")
        {
          table.push("<h4>"+data["peerinfo"][peer_uuid][0] + " <small>(" + data["peerinfo"][peer_uuid][1] + ")</small></h4>");
        }else {
          table.push("<h4>"+data["peerinfo"][peer_uuid][0]+"</h4>");
        }
        table.push("<table class='table table-hover table-condensed table-bordered'>");
        table.push("<tbody>");
        for (var i = 0; i < data["result"][peer_uuid].length; i++) 
        {
          $rows_added++;
          percent = (data["fileinfo"][peer_uuid][data["result"][peer_uuid][i][1]] * 100.00 ) / data["result"][peer_uuid][i][2];
          table.push("<tr data-peeruuid='"+peer_uuid+"' data-filename='"+btoa(data["result"][peer_uuid][i][1])+"' data-sharedir='"+btoa(data["result"][peer_uuid][i][0])+"' data-size='"+data["result"][peer_uuid][i][2]+"' data-modtime='"+data["result"][peer_uuid][i][3]+"'>");
          table.push("<td style='cursor: move'><big><b><span style='margin-right: 10px;' class='glyphicon glyphicon-file'></span> " + data["result"][peer_uuid][i][1] + "</b></big><br><small>"+ data["result"][peer_uuid][i][0]+"</small></td>");
          table.push("<td class='text-right' style='cursor:move; width: 150px;vertical-align: middle;'><span class='currentfilesize'>"+commify(data["fileinfo"][peer_uuid][data["result"][peer_uuid][i][1]])+"</span> / "+commify(data["result"][peer_uuid][i][2])+"</td>");
          table.push("</td>");
          table.push('<td style="cursor: move; width: 250px; vertical-align: middle;" class="text-center"><div style="margin-bottom: 0px" class="progress progress-striped"><div class="progress-bar" role="progressbar" style="width: '+percent+'%;"></div></div>'+percent.toFixed(2)+'%</td>');
          table.push('<td class="text-center" style="width: 40px;vertical-align: middle;"><span class="glyphicon glyphicon-minus-sign removeiteminq"></span></td>');
          table.push("</tr>");
          //console.log(data["result"][peer_uuid][i]);
        }
        table.push("</tbody></table>");
      }
      if ($rows_added == 0) { $("#downloadqempty").removeClass("hide"); };
      $("#downloadqdiv").html(table.join(""));
      $(".table tbody").sortable({helper: trhelper,start:starthelper,update:updatehelper,distance: 35}).disableSelection();
      $(".table tbody span").click(function() { });
      $(".table td span.removeiteminq").click(function(event) {
        event.stopPropagation();
        peer_uuid = $(this).closest("tr").data("peeruuid");
        modtime = $(this).closest("tr").data("modtime");
        filesize = $(this).closest("tr").data("size");
        filename = atob($(this).closest("tr").data("filename"));
        sharedir = atob($(this).closest("tr").data("sharedir"));
        console.log(peer_uuid,modtime,filesize,filename,sharedir);
        $("#removeModal #removefilename").html(filename);
        $("#removeModal #removesharedir").html(sharedir);
        $("#removeModal #removesize").html("(" + commify(filesize) + " bytes)");
        buttonthis = $(this);
        $("#removeModal #removebutton").unbind("click").click(function() {
          $('#removeModal').modal('hide');
          var $api_action = {"action":"downloadqremove","data":{"uuid":peer_uuid,"sharedir":sharedir,"filename":filename,"filesize":filesize,"filemodtime":modtime}};
          $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
          {
            if (data == 1) { buttonthis.closest("tr").fadeOut(function() { $(this).remove(); location.reload();});}
          }});

        });
        $("#removeModal").modal();
      });
      $('#downloadqdiv .table').hover(function(){ console.log("in"); $("#hoverpaused").removeClass("hide"); $dontrefresh=true; }, function(){ console.log("out"); $dontrefresh=false; $("#hoverpaused").addClass("hide");} );
      setTimeout(Update_Download_Q,500);
    }
  }});

}

$( document ).ready(function() {
  Check_For_API_Errors();
  Update_Download_Q();
  Update_Completed_Q();

});
