/*
Author    : Pradeep CH
Date      : 20-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getServers()

function getServers(){
	$('#consoleContent').html('Loading hypervisors. Please wait..').fadeIn(200)
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
                                editLink = '<a href="add.htm?uid='+this.id+'" class ="editLink" id="'+this.id+'">Edit</a>'
                                manageLink = '<a href="'+this.type+'_manager.htm?uid='+this.id+'&ip='+this.ip+'" class ="editLink" id="'+this.id+'">'+this.ip+'</a>'
				$('#servers tr:last').after('<tr><td>'+i+'</td><td>'+manageLink+'</td><td>'+this.type+'</td><td>'+this.username+'</td><td>'+editLink+'</td></tr>');
				i++;   
			}
		});
		loadResp('Hypervisors loaded successfully')
	}
}

function loadResp(resp){	
	$('#consoleContent').html(resp).fadeIn(800)
}
