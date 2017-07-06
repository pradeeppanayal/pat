/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/


getHistory();

function getHistory(){  
	loadResp('Loading history')
	target= cgiPath + 'IPSweep/historyView.py',
       	method= 'post'
       	data = {'action':'history'}
	$.triggerCall(target,method,data,loadHistory)
}

function loadHistory(resp){ 	 
	var obj = jQuery.parseJSON( resp );
	if (obj['status'] =='error'){ 
		loadResp(obj['data'])
	}else{
		content = ''
		data = obj['data'] 
		if (Object.keys(data).length == 0 ){
				loadResp('No data to load')
		}else{
			i = 1			
			$(data).each(function(){

				link = '<a href='+this.fileName+' class="historyRef" >'+this.startIp+'-'+this.endIp+'</a>'
				scanLink ='<a target=default href=ipscanner.htm?fromIP='+this.startIp+'&toIP='+this.endIp+' ">Scan</a>' 
				$('#history tr:last').after('<tr><td>'+(i++)+'</td><td>'+link+'</td><td>'+this.date+'</td><td>'+scanLink+'</td></tr>');
			});
		}  
	}

	loadResp('History loaded.')
}
//Actions

$(document).on('click', '.historyRef', function (event) { 
	event.preventDefault();  
	loadResp('Loading history')
	target= cgiPath + 'IPSweep/historyView.py',
       	method= 'post'
       	data = {'action':'loadhistory','fname':$(this).attr('href')}
	$.triggerCall(target,method,data,loadHistoryResult)
});

function loadHistoryResult(resp){
	var obj = jQuery.parseJSON( resp ); 
	content ='Status :' + obj['status']
	content +='</br>'
	content +=obj['data']
	loadResp(content)
}
function loadResp(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
