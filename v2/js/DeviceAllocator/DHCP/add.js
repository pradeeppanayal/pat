/*
Author    : Pradeep CH
Date      : 20-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


checkParam();

function checkParam(){ 
	uid = getParamValue(document.location.href,'uid') 
	if(uid==undefined){
		return
	}
	loadResp('Loading server info..') 
	$('#uid').val(uid)
	getServerInfo(uid)
}

function getServerInfo(uid){ 
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html('Loading servers. Please wait..').fadeIn(200)}) 
	target =cgiPath + 'DeviceManager/DHCP/manager.py'
	data = {'action':'loadServer','uid':uid,'uname':'','pwd':''}
	method ='POST'
	$.triggerCall(target,method,data,loadServer)
}

function loadServer(resp){ 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] ==='error'){ 
		loadResp(obj['data'])
	}
	else{   
		server = obj['data']
		$('#un').val(server.username)
		$('#pwd').val(server.password)
		$('#ip').val(server.ip)
		$('#identifier').val(server.identifier)  
		$('#status').val(server.status)  
		loadResp('Server loaded successfully')
	}
}


//Actions
$(document).on('click', '#reset', function (event) {  
	event.preventDefault(); 
	$('#un').val('')
	$('#pwd').val('')
	$('#ip').val('')
	$('#identifier').val('') 
	$('#status').val('') 
});

$(document).on('click', '#statusCheck', function (event) {  
	event.preventDefault(); 
	$('#consoleContent').html('Status check is in progress...').fadeIn(600); 
	target =cgiPath + 'DeviceManager/SystemStatus/manager.py'
	act = 'statusServer'
	data = {'action':act,'ip':$('#ip').val(),'uname':$('#un').val(),'pwd':$('#pwd').val()}
	$.triggerCall(target,'POST',data,loadStatusResp)
});

function loadStatusResp(r){
	var obj = jQuery.parseJSON( r );
	 
	if (obj['status'] ==='success'){ 
		$('#status').val(obj['data'])
		loadResp('Status check completed')
	}else{
		loadResp(obj['data'])
		$('#status').val('Failed')	
	}
}

$(document).on('click', '#save', function (event) {   
	event.preventDefault();  
	$('#consoleContent').html('Saving server info. Please wait').fadeIn(600); 
	target =cgiPath + 'DeviceManager/DHCP/manager.py'
        act='addserver'
        if($('#uid').val() != undefined && $('#uid').val()!=''){
		act = 'updateserver'
	}
	data = {'action':act,'ip':$('#ip').val(),'uname':$('#un').val(),'pwd':$('#pwd').val(),'uid':$('#uid').val(),'identifier':$('#identifier').val(),'status':$('#status').val()}
	method ='POST'
	$.triggerCall(target,method,data,loadActResp)
});
function loadActResp(resp){
	var obj = jQuery.parseJSON( resp );
	 
	if (obj['status'] ==='success'){ 
		$('#reset').click()
	}
	loadResp(obj['data'])
}
function loadResp(resp){
	$('#consoleContent').fadeOut(100,function(){$('#consoleContent').html(resp).fadeIn(600);});
}
