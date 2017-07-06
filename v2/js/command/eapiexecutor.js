
/*
Author    : Pradeep CH
Date      : 16-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/


$(document).on('click', '#execute', function (event) { 
 	loadConsoleData('Command is executing. Please wait..')
	target = cgiPath + 'command/commandExecute.py'
	method ='POST'
	ips = $('#ips').val()
	cmd = $('#cmds').val()
	username = $('#username').val()
	password = $('#password').val() 
	data = {'password':password,'ips':ips,'cmd':cmd,'username':username}
	$.triggerCall(target,method,data,loadResp)			 
});

$(document).on('click', '#reset', function (event) { 
	$('#ips').val("")
	$('#cmds').val("")
	$('#username').val("")
	$('#password').val("")
});

function loadConsoleData(c){
	$('#consoleContent').fadeOut(800,function(){$('#consoleContent').html(c).fadeIn(200)})
}
function loadResp(resp){
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] =='error'){ 
		loadConsoleData(obj['data'])
	}else{
		content = ''
		deviceResp = obj['data']
		console.log(deviceResp)
		$.each(deviceResp,function(){
			content +='<h4>' + this.ip+'</h4>' 
			content +='Status :' + this.status+'<br>'
			content +='Response :<br><pre>' + this.data+'</pre>'			
		});
		loadConsoleData(content)
	}
}
