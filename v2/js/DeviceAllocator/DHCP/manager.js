/*
Author    : Pradeep CH
Date      : 23-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/

 
checkParam();

function checkParam(){ 
	uid = getParamValue(document.location.href,'uid') 
	ip = getParamValue(document.location.href,'ip') 
	if(ip===undefined ||uid===undefined ){
		$('#manageconsole').html('Invalid request!!').fadeIn(800)
		return
	} 
	$('#uid').val(uid)
	$('#actualIp').html(ip)
        $('#actualIp').attr('href','subnetView.htm?uid='+uid+'&ip='+ip)
	$('#manageconsole').html('Loading configuration. Please wait...').fadeIn(800)
	getConfig(uid)
}
  
function getConfig(uid){ 
	target =cgiPath + 'DeviceManager/DHCP/dhcpConfigUpdater.py'
	data = {'action':'view','uid':uid}
	method ='POST'
	$.triggerCall(target,method,data,loadConfig)
}

function loadConfig(resp){ 
	var obj = jQuery.parseJSON( resp ); 
	if(obj['status']=='error'){
		loadResp(obj['data']) 	
	}else{
		loadConfigForEdit(obj['data']) 	
		loadResp('Config loaded successfully');
	}
	
}

function loadConfigForEdit(c){
	$('#dconfig').val(c)
}

function loadResp(r){
	$('#manageconsole').html(r).fadeIn(800,function(){$('#manageconsole').fadeOut(5000)})
}


//Action

$(document).on('click', '.action', function (event) {  
	$('#manageconsole').html('Processing your request. Please wait...').fadeIn(500)
	event.preventDefault();  
	action = $(this).attr('action')
	uid = $('#uid').val()
	target =cgiPath + 'DeviceManager/DHCP/dhcpConfigUpdater.py'
	if(action=='remotesave'){
		data = {'action':action,'uid':uid,'config':$('#dconfig').val()}
	}else{
		data = {'action':action,'uid':uid}
	}
	method ='POST'
	$.triggerCall(target,method,data,loadActionResp)
});

$(document).on('click', '.actionDownload', function (event) { 
	$('#manageconsole').html('Processing your request. Please wait...').fadeIn(500,function(){$('#manageconsole').fadeOut(5000)})
	event.preventDefault();  
	action = $(this).attr('action')
	target =cgiPath + 'DeviceManager/DHCP/dhcpConfigUpdater.py'
	data = {'action':action,'uid':uid}
	$.redirectPost(target,data)
});

function loadActionResp(resp){
	if(resp==undefined){
		loadResp('Empty response.') 	
		return;
	}
	try{
		var obj = jQuery.parseJSON( resp ); 
		loadResp(obj['data']) 	
	}catch(ex){
		loadResp('Something went wrong. Invalid resp')
		console.log('Response')
		console.log(resp)
	}
}
