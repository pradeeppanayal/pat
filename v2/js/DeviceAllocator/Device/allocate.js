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
	target =cgiPath  + 'DeviceManager/envmanager/envmanager.py'
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
                                $('#environment').append($('<option>',
							{
							value:this.id,
							text:this.ip+'('+this.team+')'
							}));			
			}
		});
		loadResp('Envirnment loaded successfully')
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
		$('#count').val(pool.devicecount)  
		$('#status').val( pool.status)  
		if(pool.status==='Assigned'){
			$('#action').val('release')
		}else{
			$('#action').val('assign')
		}
		$('#action').change();
		loadResp('Pool loaded successfully')
	}
}

function loadActResp(resp){ 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] ==='error'){ 
		loadResp(obj['data'])
	}
	else{   
		loadResp('<pre>'+obj['data']+'<pre>')
		$('#uid').val('')
	}
}

//Action
$(document).on('change', '#action', function (event) {		
		$('#numdays').prop('disabled', !($('#action').val()=='assign'))
		$('#environment').prop('disabled', !($('#action').val()=='assign'))
});

$(document).on('click', '#save', function (event) {   
	event.preventDefault();  
	$('#consoleContent').html('Saving changes. Please wait').fadeIn(600); 
	target =cgiPath + 'DeviceManager/Device/manager.py'
        act='savePoolEnv'
	if($('#uid').val() === undefined || $('#uid').val()===''){
		loadResp('Action not permitted')
		return
	}
	data = {'action':act,'uid':$('#uid').val(),'assignaction':$('#action').val(),'environment':$('#environment').val(),'username':$('#username').val(),'password':$('#password').val(),'numdays':$('#numdays').val(),'sanitize':$('#sanitize:checkbox:checked').length>0,'serverip':$('#dhcp').val()}
	method ='POST'
	$.triggerCall(target,method,data,loadActResp)
});


function loadResp(resp){
	$('#consoleContent').fadeOut(100,function(){$('#consoleContent').html(resp).fadeIn(600);});
}
