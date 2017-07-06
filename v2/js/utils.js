/*
Author    : Pradeep CH
Date      : 10-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

function getParamValue(url,paramName){ 
	var a = url.split('?')
	if(a.length!=2){
		return;
	}
	a = a[1].split('&')
	log(a)
	i = 0
	while(i<a.length){
		log(a[i])
		b = a[i].split('=')		
		if(paramName == b[0] ){
			return b[1]
		}
		i++;
	}
}

function log(msg){
	console.log(msg)
}
