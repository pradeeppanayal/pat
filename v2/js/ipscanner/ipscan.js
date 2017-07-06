/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

checkParam();


//Actions
$(document).on('click', '#reset', function (event) { 
	loadResp('Performing IP scan. Please wait...') 
	event.preventDefault(); 
	$('#startip').val('')
	$('#endip').val('') 
	//$('#consoleContent').html('')
});

$(document).on('click', '#scan', function (event) {   			
	startip =$('#startip').val()
	endip = $('#endip').val()
	target =cgiPath + 'IPSweep/ipsweep.py'
	method ='POST'
	data = {'startip':startip,'endip':endip}  
	$.triggerCall(target,method,data,loadResp)
	$('#reset').click()
});

function checkParam(){
	fromIP = getParamValue(document.location.href,'fromIP') 
	toIP = getParamValue(document.location.href,'toIP')  
	if(fromIP===undefined || toIP===undefined || toIP=="" || fromIP==""){
		return
	}  
	//if it's va;lid perform click 
	$('#startip').val(fromIP)
	$('#endip').val(toIP) 
	$('#scan').click()
}


function loadResp(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
