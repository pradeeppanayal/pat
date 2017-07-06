/*
Author    : Pradeep CH
Date      : 18-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

loadCA()

function loadCA(){
	loadResp('Loading CAs. Please wait...')
	$('#ca').find('option').remove().end()
	target = cgiPath + 'ssl/manager.py';
	data ={'action':"loadCA"}
	method ='POST'
	$.triggerCall(target,method,data,loadCAs)
}

function loadCAs(resp){
	if(resp==""){
		loadResp('No response recived')
		return
	}			

	var obj = jQuery.parseJSON( resp );
	if(obj['status'] == 'ERROR'){
		loadResp('Failed :' + obj['data']) 
	}else{
		if(Object.values( obj['data'])==0){
			loadResp('No CA details found. Click <a href="newca.htm">here</a> to create new CA ')
			return
		}
		i = 1 
		$(obj['data']).each(function() {
			var manageLink = '<a href="manage.htm?cn='+this.cn+'">'+this.cn+'</a>'
			$('#cas tr:last').after('<tr><td>'+i+'</td><td>'+manageLink+'</td><td>'+this.org+'</td><td>'+this.orgUnit+'</td></tr>');
			i++;    
		});
		loadResp('CAs loaded successfully')
	}
}

function loadResp(resp){
	$('#consoleContent').html(resp).fadeIn(200)
}
