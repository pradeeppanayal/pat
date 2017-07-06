/*
Author    : Pradeep CH
Date      : 16-Jun-2017
Version   : 1.0.0
Since     : 2.0.0
*/

 
checkParam();

function checkParam(){ 
	uid = getParamValue(document.location.href,'uid') 
	ip = getParamValue(document.location.href,'ip') 
	if(uid===undefined){
		showProcess('Requested information not found. Please try again.')
		return
	} 
	$('#serverId').val(uid)
	$('.serverIP').html(ip)
	showProcess('Loading devices. Please wait..')
	getDevices(uid)
}
  
function getDevices(uid){ 
	target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
	data = {'action':'loadDevices','ip':'','uname':'','pwd':'','uid':uid}
	method ='POST'
	$.triggerCall(target,method,data,loadDevices)
}

function loadDevices(resp){   
	var obj = jQuery.parseJSON(resp);
	$("#devices").empty(); 
	if(obj['status']==='success'){
		addHeader()
		$(obj['data']).each(function(){  
			addRow(this) 
		});
	}else{
		showResp(obj['data'])
	}
	showProcessMsg('Devices loaded successfully.')
}

function addHeader(){ 
	$('#devices').append('<tr><th><th><th>id</th><th>Name</th><th>Memory(MB)</th><th>vCPU</th><th>Status</th><th colspan=4></th></tr>')
}

function addRow(val){
		checkBox = '<td><td><input type="checkbox" class="select"  moid="'+val['id']+'"/ ></td>'
		id = '<td>'+val['id']+'</td>'
		name = '<td>'+val['name']+'</td>'
		status = '<td>'+val['status']+'</td>'
		ram = '<td>'+val['memory']+'</td>'
		cpu = '<td>'+val['cpu']+'</td>'
		startLink = '<td><a href="#" moid="'+ val['id']+'" action ="start" class="dact">Start</a></td>'
		stopLink = '<td><a href="#" moid="'+ val['id']+'" action ="stop"  class="dact">Stop</a></td>'
		restartLink = '<td><a href="#" moid="'+ val['id']+'" action ="restart"  class="dact">Restart</a></td>'
		consoleLink = '<td><a href="#" name="'+ val['name']+'" action ="console" moid='+val['id']+' class="console">Console</a></td>'
		detailLink = '<td><a href="VMWare_Node_details.htm?name='+val['name']+'&serverId='+$('#serverId').val()+'&serverIp='+$('.serverIP').html()+'" target="_default" >'+val['name']+'</a></td>'
		$('#devices').append('<tr>' +checkBox+id+detailLink+ram+cpu+status+startLink+stopLink+restartLink+consoleLink+'</tr>'); 			
}


//Actions
$(document).on('click', '.console', function (event) {  
	showProcess('Connecting to remote console. Please wait..')
	event.preventDefault(); 
	moid = $(this).attr('moid')
	target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
	data = {'action':'console','uid':uid,'moid':moid}
	method ='POST'
	$.triggerCall(target,method,data,showConsoleResp)
});

$(document).on('click', '.macList', function (event) {  
   event.preventDefault(); 
   window.location.href = "managemac.htm?uid="+$('#serverId').val()+"&ip="+$('.serverIP').html();
});

$(document).on('click', '.dact', function (event) {  
	showProcess('Performing action. Please wait..')
	event.preventDefault(); 
	moid = $(this).attr('moid')
	action = $(this).attr('action')
	uid = $('#serverId').val()
	target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
	data = {'action':action,'moid':moid,'uid':uid}
	method ='POST' 
	$.triggerCall(target,method,data,showActionResp)
});

$(document).on('click', '#refresh', function (event) { 
	getDevices($('#serverId').val() )
	showProcess('Refreshing..') 
});


$(document).on('click', '.resetAct', function (event) {  
	showProcess('Performing action. Please wait..')
	action = $(this).attr('action')
	devices= getSelectedDevices()
	console.log(devices.length)
	if(devices.length==0){ 
		return;
	} 
	showProcess('Loading response..')
	method ='POST'
	target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
	data = {'action':action,'devices':devices.join(),'uid':uid}  
	$.triggerCall(target,method,data,showActionResp)
});

function getSelectedDevices(){ 
	moids= []
	$('.select').each(function(i, obj) {
		if(obj.checked){ 				
			moids.push($(obj).attr('moid'))
		}
	});
				
	if(moids.length==0){
		showProcessMsg('No device(s) selected') 
	} 
        console.log(moids)
        return moids
}
$(document).on('click', '.allAct', function (event) {  
		showProcess('Performing action. Please wait..')
		action = $(this).attr('action') 
		moids= getSelectedDevices()	 
				
		if(moids.length==0){ 
			return;
		} 

		showProcess('Loading response..')
		method ='POST'
		target =cgiPath  + 'DeviceManager/Hypervisor/vmwaremanager.py'
		data = {'action':action,'moids':moids.join(),'uid':uid}  
		$.triggerCall(target,method,data,showActionResp)
});

function showResp(resp){
	$('#consoleContent').html(resp).fadeIn(1000).fadeOut(3000)
}
function showProcess(resp){
	$('#loading').html(resp).fadeIn(1000)
}
function showProcessMsg(resp){
	$('#loading').html(resp).fadeIn(1000).fadeOut(3000)
}
function showConsoleResp(resp){
	if(resp ==null || resp===""){
		showProcessMsg('Invalid Response.')
		return;
	}
	var obj = jQuery.parseJSON(resp);
	showProcessMsg(obj['data'])
}
function showActionResp(resp){
	if(resp ==null || resp===""){
		showProcessMsg('Invalid Response.')
		return;
	}
	var obj = jQuery.parseJSON(resp);	 
	showResp(obj['data']) 
        if(obj['status']==='error'){
          return;
        }
	getDevices($('#serverId').val());
	showProcess('Refreshing..') 
}
