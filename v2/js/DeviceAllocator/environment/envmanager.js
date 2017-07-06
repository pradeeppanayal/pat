/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getServers()

function getServers(){
	$('#kvmViewConsole').html('Loading environments. Please wait..').fadeIn(200)
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
                                editLink = '<a href="newserver.htm?uid='+this.id+'" class ="editLink" id="'+this.id+'">Edit</a>'
                                manageLink = '<a href="devicemapper.htm?uid='+this.id+'" class ="editLink" id="'+this.id+'">'+this.ip+'</a>'
				col1 = '<td>'+i+'</td>'
				col2 = '<td>'+manageLink+'</td>'
				col3 = '<td>'+this.team+'</td>'
				col4 = '<td>'+this.phase+'</td>'
				col5 = '<td>'+editLink+'</td>'

				$('#servers tr:last').after('<tr>'+col1+col2+col3+col4+col5+'</tr>');
				i++;   
			}
		});
		loadResp('Environments loaded successfully')
	}
}

function loadResp(resp){	
	$('#consoleContent').html(resp).fadeIn(800)
}
