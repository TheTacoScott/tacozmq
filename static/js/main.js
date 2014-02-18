function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
}

function API_Alert()
{
  $("#apialert").removeClass("hide");
}

function Check_For_API_Errors()
{
  var $api_action = {"action":"apistatus","data":""};
  $.ajax({url:"/api.post",type:"POST",data:JSON.stringify($api_action),contentType:"application/json; charset=utf-8",dataType:"json",error: API_Alert,success: function(data)
  {
    setTimeout(Check_For_API_Errors,1000);
  }
  });
}


function commify(num)
{
  num = num.toString();
  checker = /([0-9]+)([0-9]{3})/;
  while (checker.test(num)) 
  {
    num = num.replace(checker, '$1'+','+'$2');
  }
  return num;
}
