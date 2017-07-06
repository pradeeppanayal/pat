/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

 
checkParam();

function checkParam(){ 
	uid = getParamValue(document.location.href,'uid') 
	ip = getParamValue(document.location.href,'ip') 
	if(uid===undefined){
		return
	} 
	$('#managekvmip').val(uid)
	$('.managekvmip').html(ip)
	$('#managekvmconsole').html('Loading devices').fadeIn(800)
	getDevices(uid)
}
  
function getDevices(uid){ 
	target =cgiPath + 'kvm/kvmmanger.py'
	data = {'action':'loadDevices','ip':'','uname':'','pwd':'','uid':uid}
	method ='POST'
	$.triggerCall(target,method,data,loadDevices)
}

function loadDevices(resp){  
	var obj = jQuery.parseJSON(resp);
	$("#kvmdevices").empty(); 
	if(obj['status']=='OK'){
		addHeader()
		$(obj['data']).each(function(){  
			addRow(this)
		});
	}else{
		$('#managekvmconsole').html(obj['data']).fadeIn(1000)
	}
}

function addHeader(){ 
	$('#kvmdevices').append('<tr><th><th><th>id</th><th>Name</th><th>Status</th><th colspan=3></th></tr>')
}

function addRow(val){
		checkBox = '<td><td><input type="checkbox" class="select"  name="'+val['device']+'"/ ></td>'
		id = '<td>'+val['id']+'</td>'
		name = '<td>'+val['device']+'</td>'
		status = '<td>'+val['status']+'</td>'
		startLink = '<td><a href="#" name="'+ val['device']+'" action ="start" class="dact">Start</a></td>'
		stopLink = '<td><a href="#" name="'+ val['device']+'" action ="stop"  class="dact">Stop</a></td>'
		restartLink = '<td><a href="#" name="'+ val['device']+'" action ="restart"  class="dact">Restart</a></td>'
		$('#kvmdevices').append('<tr>' +checkBox+id+name+status+startLink+stopLink+restartLink+'</tr>');
		$('#managekvmconsole').html('Loading devices completed').fadeIn(800,function(){$('#managekvmconsole').fadeOut(800)})				
}


//Actions
$(document).on('click', '.dact', function (event) {  
	$('#managekvmconsole').html('Performing action. Please wait..')
	event.preventDefault(); 
	deviceName = $(this).attr('name')
	action = $(this).attr('action')
	uid = $('#managekvmip').val()
	target =cgiPath + 'kvm/kvmmanger.py'
	data = {'action':action,'device':deviceName,'uid':uid}
	method ='POST'
	$.triggerCall(target,method,data,showActionResp)
});

$(document).on('click', '.allAct', function (event) {  
		$('#managekvmconsole').html('Performing action. Please wait..')
		action = $(this).attr('action')
		count = 0
		devices= []
		$('.select').each(function(i, obj) {
			if(obj.checked){
    				count +=1					
				devices.push(obj.name)
			}
		});
				
		if(count==0){
			$('#managekvmconsole').html('No device(s) selected').fadeIn(100);
			return;
		} 

		$('#managekvmconsole').fadeOut(100,function(){$('#managekvmconsole').html('Loading response').fadeIn(1000);});  
		method ='POST'
		target =cgiPath + 'kvm/kvmmanger.py'
		data = {'action':action,'devices':devices.join(),'uid':uid}  
		$.triggerCall(target,method,data,showActionResp)
});


function showActionResp(resp){
	$('#managekvmconsole').html(resp).fadeIn(1000,function(){
			getDevices($('#managekvmip').val());
			$('#managekvmconsole').html('Refreshing').fadeOut(3000)
	});
}
