/*
Author    : Pradeep CH
Date      : 18-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

//Actions
$(document).on('click', '#reset', function (event) {  
	event.preventDefault(); 
	cn = $('#cn').val('')
	email = $('#email').val('')
	country = $('#country').val('')
	org = $('#org').val('')
	state = $('#state').val('')
	locality = $('#locality').val('')
	orgUnit = $('#orgUnit').val('')
});

$(document).on('click', '#save', function (event) {   
	event.preventDefault(); 
	loadResp('Creating CA. Please wait..')
	
	cn = $('#cn').val()
	email = $('#email').val()
	country = $('#country').val()
	org = $('#org').val()
	state = $('#state').val()
	locality = $('#locality').val()
	orgUnit = $('#orgUnit').val()
	
	target = cgiPath + 'ssl/manager.py' 
	data = {'action':'addCA','cn':cn,'email':email, 'country':country,'org':org,'state':state,'locality':locality,'orgUnit':orgUnit};
	method ='POST'

	$.triggerCall(target,method,data,showResp)
	$('#reset').click()
});

function showResp(resp){
	console.log('recived')
	var obj = jQuery.parseJSON( resp ); 
	loadResp(obj['data']) 
}
function loadResp(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
