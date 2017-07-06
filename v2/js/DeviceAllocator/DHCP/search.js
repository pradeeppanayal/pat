/*
Author    : Pradeep CH
Date      : 23-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/
 
$(document).on('click', '#search', function (event) {  
	$('#searchResult').html('Search in progress please wait').fadeIn(1000)
	event.preventDefault(); 
	keyword =$('#keyword').val()
	force = $('#force').prop('checked')
	$('#consoleContent').html('Saving server info. Please wait').fadeIn(600); 
	target =cgiPath + 'DeviceManager/DHCP/search.py'
	data = {'keyword':keyword,'force':force}  
	method ='POST'
	$.triggerCall(target,method,data,showResp) 
});

function showResp(resp){         
	var obj = jQuery.parseJSON( resp );  
	$('#searchResult').html(obj['data']).fadeIn(1000)
}
