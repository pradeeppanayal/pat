/*
Author    : Pradeep CH
Date      : 19-Jun-2017
Version   : 1.0.0
Since     : 2.0.0
*/

init();

function init(){
	sid = getParamValue(document.location.href,'id') 
        console.log(sid)
        console.log('data')
	//sname = getParamValue(document.location.href,'name') 
	if(sid===undefined){
		loadResp('Invalid request..') 
		return
	}
	//$('#scriptName').val(sname)
	$('#scriptId').val(sid)
    	loadResp('Loading script details...')
        loadScriptInfo(sid);
}

function loadScriptInfo(sid){
	target =cgiPath + 'scripter/scriptmanager.py'
	data = {'action':'getScriptInfo','id':$('#scriptId').val()}
	method ='POST'
	$.triggerCall(target,method,data,loadScriptInfoResp)
}

function loadScriptInfoResp(r){
  if(r===undefined){
    loadResp('Invalid resp')
    return
  }
 var obj = jQuery.parseJSON( r );
  if(obj['status']==='success'){
    $('#scriptName').val(obj['data'].fileName)
    $('#arg').attr('placeholder',obj['data'].param)
    loadResp('Script info loaded successfully')
  } else{
    loadResp(obj['data'])
 }
}
//Actions 
$(document).on('click','#reset',function(){
	$('#ip').val('')
	$('#arg').val('')
	$('#username').val('')
	$('#password').val('')
});

$(document).on('click','#submit',function(){
	event.preventDefault(); 
	ip = $('#ip').val()
	username = $('#username').val()
	password = $('#password').val()
	arg = $('#arg').val()
	id = $('#scriptId').val()

	$('#savekvmconsole').html('Saving server info. Please wait').fadeIn(600); 
	target =cgiPath + 'scripter/scriptmanager.py'
	data = {'action':'execute','ip':ip,'username':username,'password':password,'id':id,'arg':arg}
	method ='POST'
	$.triggerCall(target,method,data,loadActResp)
	$('#reset').click()
});

function loadActResp(resp){
  if(resp===undefined){
    loadResp('Invalid resp')
    return
  }
  var obj = jQuery.parseJSON( resp );
  console.log(obj['status']==='success')
  if(obj['status']==='success'){
    $('#reset').click();
    loadResp('Execution completed. Response : <pre>'+obj['data']+'</pre>') 
  } else{
  	loadResp(obj['data']) 
  }
}

function loadResp(resp){
	$('#consoleContent').html(resp).fadeIn(600);
}
