/*
Author    : Pradeep CH
Date      : 20-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getServers()

function getServers(){
	$('#consoleContent').html('Loading servers. Please wait..').fadeIn(200)
	target =cgiPath  + 'DeviceManager/DHCP/manager.py'
	data = {'action':'loadservers'}
	method ='POST'
	$.triggerCall(target,method,data,loadServers)
}
$(document).on('click', '.synch', function (event) {   
	event.preventDefault();  
	$('#consoleContent').html('Synchrinization is in progress. Please wait').fadeIn(600); 
	id= $(this).attr('id')
	target =cgiPath + 'DeviceManager/DHCP/configManager.py'         
	data = {'action':'synch','uid':id}
	method ='POST'
	$.triggerCall(target,method,data,loadActResp)
});

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
                                manageLink = '<a href="manager.htm?uid='+this.id+'&ip='+this.ip+'" class ="editLink" id="'+this.id+'">'+this.ip+'</a>'
                                synchLink = '<a class ="synch" id="'+this.id+'">Synch</a>'
				col1 = '<td>'+i+'</td>'
				col2 = '<td>'+manageLink+'</td>'
				col3 = '<td>'+this.username+'</td>'
				col4 = '<td>'+this.identifier+'</td>'
				col5 = '<td>'+this.status+'</td>'
				col6 = '<td>'+this.configAvailable+'</td>'
				col7 = '<td>'+this.configStatus+'</td>'
				col8 = '<td>'+synchLink+'</td>'
				col9 = '<td>'+editLink+'</td>'
				$('#servers tr:last').after('<tr>'+col1+col2+col3+col4+col5+col6+col7+col8+col9+'</tr>');
				i++;   
			}
		});
		loadResp('DHCP servers loaded successfully')
	}
}
function loadActResp(resp){
	var obj = jQuery.parseJSON( resp ); 
	if(data['status']==='success'){
		getServers();
	}
	loadResp(obj['data'])
}
function loadResp(resp){	
	$('#consoleContent').html(resp).fadeIn(800)
}
