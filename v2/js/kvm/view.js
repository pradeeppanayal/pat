/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getServers()

function getServers(){
	$('#kvmViewConsole').html('Loading servers. Please wait..').fadeIn(200)
	target =cgiPath + 'kvm/kvmmanger.py'
	data = {'action':'loadServers','ip':'','uname':'','pwd':''}
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
				var editLink = '<a href="newkvm.htm?uid='+this.id+'&ip='+this.ip+'" class="kvmserveredit">Edit</a>'
				var manageLink = '<a href="manage.htm?uid='+this.id+'&ip='+this.ip+'" class="kvmserveredit">'+this.ip+'</a>'
				$('#kvmservers tr:last').after('<tr><td>'+i+'</td><td>'+manageLink+'</td><td>'+this.username+'</td><td>'+editLink+'</td></tr>');
				i++;   
			}
		});
		loadResp('Servers loaded successfully')
	}
}

function loadResp(resp){	
	$('#kvmViewConsole').html(resp).fadeIn(800)
}
