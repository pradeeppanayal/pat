/*
Author    : Pradeep CH
Date      : 06-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/

$(document).on('click', '#submit', function (event) {  
   	keyword= $('#keyword').val()
	showConsole('Searching...')
	target =cgiPath + 'library/manage.py'
	data = {'action':'search','keyword':keyword}
	method ='POST' 
	$.triggerCall(target,method,data,loadResp)
}); 

//perform a default search
$('#submit').click()


$(document).on('click', '.actdownload', function (event) {  
	target =cgiPath + 'library/manage.py'
	data = {'action':'download','fname':$(this).attr('fname')}
	$.redirectPost(target,data)
}); 
$(document).on('click', '.actdelete', function (event) {  
	target =cgiPath + 'library/manage.py'
	data = {'action':'delete','fname':$(this).attr('fname')}
	$.triggerCall(target,method,data,loadDelResp)
}); 

function loadDelResp(resp){
 if(resp===undefined){
    showConsole('Invalid resp')
    return
  }

  var obj = jQuery.parseJSON( resp );
  if(obj['status']=='error'){
     showConsole(obj['data'])
  }else{  
	$('#submit').click();
  }
}
function loadResp(resp){
  if(resp===undefined){
    showConsole('Invalid resp')
    return
  }

  var obj = jQuery.parseJSON( resp );
  if(obj['status']=='error'){
     showConsole(obj['data'])
  }else{  
     if(obj['data'].length==0){
        showConsole('No match found')
	return
     }
     play= "<img src='/pat/v2/img/play.png'  style='width:20px' title='Play'/>"
     download= "<img src='/pat/v2/img/download.png'  style='width:20px' title='Download' />"
     deleteImg= "<img src='/pat/v2/img/delete.png'  style='width:20px' title='Delete'  />"
     view= "<img src='/pat/v2/img/view.png'  style='width:20px' title='View' />"
     
     c ='';
     $.each(obj['data'],function(){
	
	c += "<div class='mediaItem'>"
		
	c +="	<span class='boxLeft'><img src='/pat/v2/img/"+this['mediatype']+".png' width='100%' height='100%' /></span>"
	c +="	<div class='boxRight'>"
	c +="		<span class='title'>"+this['subject']+"</span>"
	c +="		<span class='body'>"+this['desc']+"</span>"
	c +="		<span class='date'>"+this['date']+"</span>"
	c +="		<span class='type'>"	
	c += '			<span id="mediaAction">'
	
	if(this['mediatype']==='video' || this['mediatype']=== 'audio'){
		c +='<span class="play"><a target="new" href="/pat/v2/library/mediaViewer.htm?url='+this['path']+'&type='+this['mediatype']+'">'+play+'</a></span>' 
	}else if(this['mediatype']=== 'image'){
		c +='<span class="view"><a target="new" href="/pat/v2/library/mediaViewer.htm?url='+this['path']+'&type='+this['mediatype']+'">'+view+'</a></span>'
	}else if(this['mediatype']==='pdf'){
		c +='<span class="view"><a target="new" href="'+this['path']+'">'+view+'</a></span>'
	}
	c +='			<span class="view"><a class="actdownload" href="#" fname="'+this['filename']+'">'+download+'</a></span>'
	c +='			<span class="view"><a class="actdelete" href="#" fname="'+this['filename']+'">'+deleteImg+'</a></span>'
	c +="			</span>"
	c +="		</span>"
	c +="	</div>"
	c +="</div>"


     });
    showConsole(c)
  }
}
function showConsole(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
