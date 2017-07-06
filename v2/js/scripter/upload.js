/*
Author    : Pradeep CH
Date      : 19-Jun-2017
Version   : 1.0.0
Since     : 2.0.0
*/
 

//Actions 

$(document).on('change','#uploadScript',function(){
   var files= $('#uploadScript')[0].files
   if(files.length==0){
      $('#fileLabel').val('Select a script file');
      return
   }
   $('#fileLabel').val(files[0].name);
});

$(document).on('click', '#submit', function (event) {  
    event.preventDefault(); 
	
   loadResp('Uploading script. Please wait...')
   event.preventDefault();
   var files= $('#uploadScript')[0].files
   if(files.length==0){
      loadResp('No script selected')
      return
   }
   var file = files[0]
   var data = new FormData();
   data.append('script', file)
   data.append('action', 'upload')
   data.append('scriptname', $('#scriptname').val())
   data.append('username', $('#username').val())
   data.append('password', $('#password').val())  
   data.append('scriptType', $('#scriptType').val())  
   data.append('param', $('#param').val())  
   target = cgiPath +'scripter/scriptmanager.py'
   $.triggerPOSTCallWithoutContentType(target,data,loaActResp);
});


$(document).on('click', '#submit', function (event) {  
    event.preventDefault(); 
    $('#scriptname').val('')
    $('#username').val('')
    $('#password').val('')
    $('#scriptType').val('')
    $('#param').val('')
    $('#uploadScript').val('')
    $('#fileLabel').val('');
});
function loaActResp(resp){
  if(resp===undefined){
    loadResp('Invalid resp')
    return
  }
  var obj = jQuery.parseJSON( resp );
  if(obj['status']==='success'){
    $('#reset').click();
  } 
  loadResp(obj['data']) 
}
function loadResp(resp){
	$('#consoleContent').html(resp).fadeIn(1000);
}
