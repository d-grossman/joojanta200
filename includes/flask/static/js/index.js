$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
		  	console.log(response);

                        var json = JSON.parse(response);
			var _ret = json['ret'];
 			var _msg = json['msg'];

			console.log('response');
			console.log(_ret);
			console.log(_msg);
	                if (_ret === 'True'){
                        $("#topImage").html("<img height=\"294\" width=\"458\" src=\""+ json['topImage'] + "\"\>");
				console.log('top');
                        $("#bottomImage").html("<img height=\"294\" width=\"458\" src=\""+ json['bottomImage'] + "\"\>");
				console.log('bottom');
			} else {
                        $("#topImage").html("WARNING: " + _msg);
				console.log('error');
			}
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
