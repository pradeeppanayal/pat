/*
Author    : Pradeep CH
Date      : 06-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/

$(document).on('click', '#submit', function (event) {  
   showConsole('Uploading file. Please wait...')
   event.preventDefault();
   var files= $('#sourcefile')[0].files
   if(files.length==0){
      showConsole('No file selected')
      return
   }
   var file = files[0]
   var data = new FormData();
   data.append('sourcefile', file)
   data.append('name', $('#name').val())
   data.append('subject', $('#subject').val())
   data.append('desc', $('#desc').val())
   data.append('action', 'upload')  
   data.append('mediatype', $('#mediatype').val())  
   target = cgiPath +'library/manage.py'
   $.triggerPOSTCallWithoutContentType(target,data,loadPushResp);
});
$(document).on('change','#sourcefile',function(){

   $('#name').val('')
   var files= $('#sourcefile')[0].files
   if(files.length==0){
      $('#fileLabel').val('Select an image file');
      return
   }
   $('#fileLabel').val(files[0].name);
	autoSelect(files[0].name);
});
function autoSelect(fileName){
	$('#name').val(fileName)	
	slashIndex = fileName.lastIndexOf('/')
        fname = fileName
        if(slashIndex>-1){
		fname = fileName.substring(slashIndex)
	}
	dotindex = fname.lastIndexOf('.')
	extension = ''
	if(dotindex>-1 && dotindex+1<fname.length){
		extention = fname.substring(dotindex+1)
	}
	if(extention == ''){
		return;	
	}
	if( extention.toLowerCase() === 'pdf' ){
		$('#mediatype').val('pdf')
	}else if (['mp4','avi','mkv'].includes(extention.toLowerCase())){
		$('#mediatype').val('video')	
	}else if (['jpg','jpeg','png','gif'].includes(extention.toLowerCase())){
		$('#mediatype').val('image')
	}else if (['mp3','ogg','wav'].includes(extention.toLowerCase())){
		$('#mediatype').val('audio')
	}else{
		$('#mediatype').val('other')
	}
	

}

function loadPushResp(resp){
  if(resp===undefined){
    loadResp('Invalid resp')
    return
  }

  var obj = jQuery.parseJSON( resp );
  if(obj['status']=='error'){
     showConsole(obj['data'])
  }else{  
     $('#reset').click()
     showConsole(obj['data'])
  }
}
function showConsole(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
