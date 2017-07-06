
/*
Author    : Pradeep CH
Date      : 22-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/


$(document).on('click', '#submit', function (event) {  
   loadResp('Pushing image. Please wait...')
   event.preventDefault();
   var files= $('#uploadImg')[0].files
   if(files.length==0){
      loadResp('No images selected')
      return
   }
   var file = files[0]
   var data = new FormData();
   data.append('imgFile', file)
   data.append('ips', $('#ips').val())
   data.append('uname', $('#username').val())
   data.append('password', $('#password').val()) 
   data.append('cgipath', cgiPath) 
   target = cgiPath +'command/imagepush.py'
   $.triggerPOSTCallWithoutContentType(target,data,loadPushResp);
});
$(document).on('change','#uploadImg',function(){
   var files= $('#uploadImg')[0].files
   if(files.length==0){
      $('#fileLabel').val('Select an image file');
      return
   }
   $('#fileLabel').val(files[0].name);
});
function loadPushResp(resp){
  if(resp===undefined){
    loadResp('Invalid resp')
    return
  }

  var obj = jQuery.parseJSON( resp );
  if(obj['status']=='error'){
     loadResp(obj['data'])
  }else{ 
      content = ""
      keys = Object.keys(obj['data'])
      $(keys).each(function() { 
          currentData = obj['data'][this] 
	  content += '<h4>'+this+'</h4>'
	  content += '<pre>'+currentData+'</pre>'
      });
     loadResp(content)
  }
}
function loadResp(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}

