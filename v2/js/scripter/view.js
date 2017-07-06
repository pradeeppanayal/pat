/*
Author    : Pradeep CH
Date      : 19-Jun-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getScripts()

function getScripts(){ 
 	loadResp('Loading scripts. Please wait..')
	target =cgiPath + 'scripter/scriptmanager.py'
	data = {'action':'getScripts'}
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
				var executeLink = '<a href="executor.htm?id='+this.id+'">Execute</a>'
 				var col1 = '<td>'+i+'</td>'
 				var col2 = '<td>'+this.fileName+'</td>'
 				var col3 = '<td>'+this.uploadedBy+'</td>'
 				var col4 = '<td>'+this.uploadedOn+'</td>'
 				var col5 = '<td>'+executeLink+'</td>'
				$('#scripts tr:last').after('<tr>'+col1+col2+col3+col4+col5+'</tr>');
				i++;   
			}
		});
		loadResp('Scripts loaded successfully')
	}
}

function loadResp(resp){	
	$('#consoleContent').html(resp).fadeIn(800)
}
