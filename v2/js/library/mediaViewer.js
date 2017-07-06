/*
Author    : Pradeep CH
Date      : 06-May-2017
Version   : 1.0.0
Since     : 2.0.0
*/


checkParam();

function checkParam(){ 
	url = getParamValue(document.location.href,'url')
	type = getParamValue(document.location.href,'type') 
	if(url==undefined || type==undefined){
		showContent('<h4>No media to load. Please check the URL</h4>');
		return;
	}

	if(type === 'video'){
		loadVideoPlayer(url)
	}else if(type ==='audio'){
		loadAudioPlayer(url)
	}else if(type==='image'){
		showimage(url)
	}
}


function loadVideoPlayer(url){
	c = '<video class="videoPlayer" controls> <source src ='+url+' >Your browser does not support video player. Try downloafing</audio>'
	showContent(c)
}
function loadAudioPlayer(url){
        c = '<div style="margin-top:10%; "><center>'
	c += '<audio controls> <source src ='+url+' type="audio/mpeg">Your browser does not support audio player. Try downloafing</audio>'
	c +='</center></div>'
	
	showContent(c)
}
function showimage(url){
        c = '<div style="margin-top:2%; "><center>'	
	c += '<img src='+url+' style="max-height:550px" alt="Image">'
	c +='</center></div>'
	showContent(c)
}

function showContent(c){
	$('#mediaContent').html(c);	
}


