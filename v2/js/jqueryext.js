//Jquery extention file
/*

Author  : Pradeep CH
Version : 1.0.0
Since   : 1.0.0
Date    : Sat Feb 4 2017

This file extends jquery to add two more feture to trigger post call and a API hit
*/

$.extend({
    		redirectPost: function(location, args)
    		{
        		var form = $('<form></form>');
       	 		form.attr("method", "post");
        		form.attr("action", location);
        		form.attr("target", 'default');

        		$.each( args, function( key, value ) {
            			var field = $('<input></input>');

           			field.attr("type", "hidden");
            			field.attr("name", key);
            			field.attr("value", value);

            			form.append(field);
        		});
       			$(form).appendTo('body').submit();
    		},

		triggerCall : function(target,method,bodyContent,targetMethod){
			$.ajax({
       				url: target,
       				type: method,
       				data: bodyContent,
       				success: function(response, status, xhr){  
					targetMethod(response);
				}
			});  
		},
		triggerPOSTCallWithoutContentType : function(target,bodyContent,targetMethod){
			$.ajax({
				url: target,
       				data: bodyContent,
    				cache: false,
   				contentType: false,
    				processData: false,
    				type: 'POST',
       				success: function(response, status, xhr){  
					targetMethod(response);
				}
			});  
		}
});
