/*
Author    : Pradeep CH
Date      : 10-Feb-2017
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
	$('#updateKVMServerID').val(uid)
	getServerInfo(uid)
}

function getServerInfo(uid){ 
	$('#kvmViewConsole').fadeOut(800,function(){$('#kvmViewLoading').html('Loading servers. Please wait..').fadeIn(200)}) 
	target =cgiPath + 'kvm/kvmmanger.py'
	data = {'action':'loadServer','uid':uid,'uname':'','pwd':''}
	method ='POST'
	$.triggerCall(target,method,data,loadServer)
}

function loadServer(resp){ 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] =='error'){ 
		loadResp(obj['data'])
	}
	else{   
		server = obj['data']
		$('#newkvmip').val(server.ip)
		$('#newkvmusername').val(server.username)
		$('#newkvmpassword').val(server.password)
		loadResp('Server loaded successfully')
	}
}


//Actions
$(document).on('click', '#newkvmreset', function (event) {  
	event.preventDefault(); 
	$('#newkvmip').val('')
	$('#newkvmusername').val('')
	$('#newkvmpassword').val('')
});

$(document).on('click', '#savekvmserver', function (event) {  
	event.preventDefault(); 
	ip = $('#newkvmip').val()
	username = $('#newkvmusername').val()
	password = $('#newkvmpassword').val()
	$('#savekvmconsole').html('Saving server info. Please wait').fadeIn(600); 
	target =cgiPath + 'kvm/kvmmanger.py'
	data = {'action':'add','ip':ip,'uname':username,'pwd':password,'uid':$('#updateKVMServerID').val()}
	method ='POST'
	$.triggerCall(target,method,data,loadResp)
	$('#newkvmreset').click()
});

function loadResp(resp){
	$('#savekvmconsole').fadeOut(100,function(){$('#savekvmconsole').html(resp).fadeIn(600);});
}
