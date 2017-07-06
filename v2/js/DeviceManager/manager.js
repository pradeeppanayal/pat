
/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/
checkParam();

function checkParam(){
	fromIP = getParamValue(document.location.href,'fromIP') 
	toIP = getParamValue(document.location.href,'toIP') 
	if(fromIP===undefined || toIP===undefined || toIP=="" || fromIP==""){
		return
	} 
	//if it's va;lid perform click
	$('#resetDeviceIPs').val(fromIP+'-'+toIP) 
	//$('resetDevice').trigger( "click" );
}

$(document).on('click', '#resetDevice', function (event) { 
	$('#deviceResetconsoleResult').html('Reset in progress. Please wait..').fadeIn(800)
	target =cgiPath +  'deviceaction/deviceReset.py'
	method ='POST'
	data = {'username':$('#resetDeviceUsername').val(),'pwd':$('#resetDevicePassword').val(),'ips':$('#resetDeviceIPs').val()}  
	$.triggerCall(target,method,data,loadResp)			 
});

$(document).on('click', '#resetDeviceReset', function (event) { 
	$('#resetDeviceUsername').val("")
	$('#resetDevicePassword').val("")
	$('#resetDeviceIPs').val("")
});

function loadResp(resp){
	$('#deviceResetconsoleResult').html(resp).fadeIn(200);
}
