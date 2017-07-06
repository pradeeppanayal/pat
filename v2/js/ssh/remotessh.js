/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

$(document).on('click', '#doremotessh', function (event) {  
	$('#remoteSSHconsoleResult').html("").fadeOut(100,function(){$('#remoteSSHloading').fadeIn(1000);});
	target =cgiPath + 'ssh/remotessh.py'
	method ='POST'
	data = {'username':$('#username').val(),'ip':$('#ip').val()}  
	$.triggerCall(target,method,data,loadResp)			 
});

$(document).on('click', '#resetremotessh', function (event) {  
	$('#username').val("")
	$('#ip').val("")
});

function loadResp(resp){
	$('#remoteSSHloading').fadeOut(800,function(){$('#remoteSSHconsoleResult').html(resp).fadeIn(200)})
}
