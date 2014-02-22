function ShutDownSuccess()
{
  $('#shutdowncomplete').modal();
  $('.jumbotron').fadeOut();
  $('.navbar').fadeOut();
  $('footer').fadeOut();
}
function ShutDown()
{
  $.ajax({url:"/shutitdown",type:"GET",error:ShutDownSuccess,success: function(data) { setTimeout(ShutDown,1000);}});
}
$( document ).ready(function() {
  ShutDown();
});

