/*
Author    : Pradeep CH
Date      : 13-Feb-2017
Version   : 1.0.0
Since     : 2.0.0
*/

 
checkParam();

function checkParam(){ 
	cn = getParamValue(document.location.href,'cn')  
	if(cn=== undefined ){
		$('#manageconsole').html('Invalid request!!').fadeIn(800)
		return
	}  
	$('#orginalCa').html(cn) 
	$('#csrCA').val(cn) 
} 

//Action
//CA CERTS
$(document).on('click', '.caAct', function (event) {
	ca = $('#orginalCa').html()
	act = $(this).attr('act')
	target = cgiPath + 'ssl/manager.py' 
	data = {'ca':ca,'action':act}
	$.redirectPost(target,data);
});

//USER CERT
$(document).on('click', '#GenerateUserCert', function (event) {
	ca = $('#orginalCa').html()
	act = $(this).attr('act')
	username = $('#username').val()
	target = cgiPath + 'ssl/manager.py' 
	data = {'ca':ca,'action':act,'username':username}
	$.redirectPost(target,data);
	$('#username').val('')
});

//DEVICE CERT   
$(document).on('click', '#GenerateDeviceCert', function (event) {
	ca = $('#orginalCa').html()
	act = $(this).attr('act')
	deviceName = $('#deviceName').val()
	target = cgiPath + 'ssl/manager.py' 
	data = {'ca':ca,'action':act,'deviceName':deviceName}
	$.redirectPost(target,data);
	$('#deviceName').val('')
});

$(document).on('change','#csrFile',function(){
   var files= $('#csrFile')[0].files
   if(files.length==0){
      $('#fileLabel').val('Select an CSR file');
      return
   }
   $('#fileLabel').val(files[0].name);
});

//CSR CERT
/*
$(document).on('click', '#signCSR', function (event) {
	ca = $('#orginalCa').html()
	act = $(this).attr('act')
	csrFile = $('#csr')[0].files[0]
	if(csrFile === undefined){
		alert('Upload a CSR')
		return
	}
	target = cgiPath + 'ssl/manager.py' 
	data = {'ca':ca,'action':act,'csrFile':csrFile}
	$.redirectPost(target,data);
	$('#deviceName').val('')
});
*/
function loadResp(resp){
	 $('#consoleContent').html(resp).fadeIn(600); 
}
