/*
Author    : Pradeep CH
Date      : 21-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


checkParam();

function checkParam(){ 
	uid = getParamValue(document.location.href,'id') 
	if(uid===undefined){
		return
	}
	loadResp('Loading pool info..') 
	$('#uid').val(uid)
	loadHypervisor();
	loadPoolInfo(uid);
}
 
function loadHypervisor(uid){ 
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html('Loading hypervisors. Please wait..').fadeIn(200)}) 
	target =cgiPath  + 'DeviceManager/Hypervisor/manager.py'
	data = {'action':'loadservers'}
	method ='POST'
	$.triggerCall(target,method,data,loadServers)
}


function loadServers(resp){  
	var obj = jQuery.parseJSON( resp );
	 
	if (obj['status'] =='error'){ 
		loadResp(obj['data'])
	}
	else{  
		i = 1 
		$(obj['data']).each(function() {
			if(this != undefined && this.ip != undefined){    
                                $('#hypervisor').append($('<option>',
							{
							value:this.ip,
							text:this.ip+'('+this.type+')'
							}));			
			}
		});
		loadResp('Hypervisors loaded successfully')
	}
}

function loadPoolInfo(uid){ 
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html('Loading pool info. Please wait..').fadeIn(200)}) 
	target =cgiPath + 'DeviceManager/Device/manager.py'
	data = {'action':'getPool','uid':uid}
	method ='POST'
	$.triggerCall(target,method,data,loadPool)
}


function loadPool(resp){ 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] ==='error'){ 
		loadResp(obj['data'])
		$('#uid').val('')
	}
	else{   
		pool = obj['data']
		$('#dhcp').val(pool.serverIp)
		$('#pool').val(pool.rangeStart+'-'+pool.rangeEnd)  
		loadResp('Pool loaded successfully')
	}
}

function loadActResp(resp){ 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] ==='error'){ 
		loadResp(obj['data'])
	}
	else{   
		loadResp(obj['data'])
	}
	$('#uid').val('')
}

//Action
$(document).on('click', '#save', function (event) {   
	event.preventDefault();  
	$('#consoleContent').html('Saving changes. Please wait').fadeIn(600); 
	target =cgiPath + 'DeviceManager/Device/manager.py'
        act='savePoolHypervisor'
	if($('#uid').val() === undefined || $('#uid').val()===''){
		loadResp('Action not permitted')
		return
	}
	data = {'action':act,'uid':$('#uid').val(),'hypervisor':$('#hypervisor').val()}
	method ='POST'
	$.triggerCall(target,method,data,loadActResp)
});


function loadResp(resp){
	$('#consoleContent').fadeOut(100,function(){$('#consoleContent').html(resp).fadeIn(600);});
}
