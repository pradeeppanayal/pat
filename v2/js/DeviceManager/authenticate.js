
/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

checkParam();

function checkParam(){
	fromIP = getParamValue(document.location.href,'fromIP') 
	toIP = getParamValue(document.location.href,'toIP') 
	if(fromIP===undefined || toIP===undefined || toIP=="" || fromIP==""){
		return
	} 
	//if it's va;lid perform click
	$('#ValAuthips').val(fromIP+'-'+toIP) 
	//$('ValAuthsubmit').trigger( "click" );
}

$(document).on('click', '#ValAuthsubmit', function (event) { 
	$('#ValAuthconsoleResult').html("Authentication in progress. Please wait...").fadeIn(800);			
	keyword =$('#keyword').val()
	force = $('#force').prop('checked')
	target = cgiPath + 'deviceaction/authenticationValidator.py'
	method ='POST'
	data = {'username':$('#ValAuthusername').val(),'pwd':$('#ValAuthpwd').val(),'ips':$('#ValAuthips').val()}  
	$.triggerCall(target,method,data,loadResp)			 
});

$(document).on('click', '#ValAuthReset', function (event) { 
	$('#ValAuthusername').val("")
	$('#ValAuthpwd').val("")
	$('#ValAuthips').val("")
});

function loadResp(resp){
	$('#ValAuthconsoleResult').html(resp).fadeIn(800); 
}
