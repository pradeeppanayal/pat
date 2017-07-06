/*
Author    : Pradeep CH
Date      : 21-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getPools()

function getPools(){
	$('#consoleContent').html('Loading pools. Please wait..').fadeIn(200)
	target =cgiPath  + 'DeviceManager/Device/manager.py'
	data = {'action':'getPools'}
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
			if(this != undefined){    
				col1 = '<td>'+i+'</td>'
				col2 = '<td>'+this.rangeStart+'-'+this.rangeEnd+'</td>'
				col3 = '<td>'+this.serverIp+'</td>'
				col4 = '<td>'+this.subnetMask+'</td>'
				col5 = '<td>'+this.devicecount+'</td>'
				col6 = '<td>'+'<a target="_blank" title="Click to Assign/Release Devices" href="allocate.htm?id='+this.poolid+'">'+this.status+'</a>'+'</td>'
				col7 = '<td>'+this.envip+'</td>'
				col8 = '<td>'+'<a target="_blank" title="Click to Add/Modify Hypervisor" href="hypervisormapper.htm?id='+this.poolid+'">'+this.hypervisor+'</a>'+'</td>'
				col9 = '<td>'+this.assignEndDate+'</td>'
				
				$('#servers tr:last').after('<tr>'+col1+col2+col3+col4+col5+col6+col7+col8+col9+'</tr>');
				i++;   
			}
		});
		loadResp('Pools loaded successfully')
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
