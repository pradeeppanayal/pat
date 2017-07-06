/*
Author    : Pradeep CH
Date      : 10-Mar-2017
Version   : 1.0.0
Since     : 2.0.0
*/
 
checkParam();

function checkParam(){ 
	serverIp = getParamValue(document.location.href,'serverIp') 
	serverId = getParamValue(document.location.href,'serverId') 
	deviceName = getParamValue(document.location.href,'name') 

	if(serverId===undefined || serverIp==undefined || deviceName==undefined){
		showProcess('Requested information not found. Cause : Invalid URL. Please try again...')
		return
	} 
	$('#serverId').val(serverId)
	link='<a title="Go back to the VMWare device manager page." href="manage.htm?uid='+ serverId+'&ip='+serverIp+'">'+serverIp+'</a>'
	$('#serverBackLink').html(link)
	$('.deviceName').html(deviceName)
	showProcess('Loading device information. Please wait..') 
	loadDeviceInfo(serverId,deviceName)
}

function loadDeviceInfo(serverId,deviceName){
	target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
	data = {'action':'loadDeviceInfo','deviceName':deviceName,'uid':serverId} 
	$.triggerCall(target,'post',data,loadResp) 
}

function loadResp(resp){
	if(resp ==null || resp===""){
		showProcessMsg('Invalid Response.')
		return;
	}
	var obj = jQuery.parseJSON(resp); 
	if(obj['status']==='error'){
		showProcess(obj['data'])
		return
	}

	$(obj['data']).each(function() {
		col1 = '<td>'+this['key']+'</td>'
		col2 = '<td>'+this['val']+'</td>' 
		row = '<tr>'+col1+col2+'</tr>'
		$('#devices').append(row); 
	});
	showProcessMsg('Information loaded successfully.')
}



function showProcess(resp){
	$('#loading').html(resp).fadeIn(1000)
}

function showProcessMsg(resp){
	$('#loading').html(resp).fadeIn(1000).fadeOut(3000)
}

//Action
$(document).on('click', '#close', function (event) {  
	open(location, '_self').close();
});
   
