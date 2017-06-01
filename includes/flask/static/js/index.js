$(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
                        var json = JSON.parse(response);
				console.log('response');
                        $("#topImage").html("<img height=\"294\" width=\"458\" src=\""+ json['topImage'] + "\"\>");
				console.log('top');
                        $("#bottomImage").html("<img height=\"294\" width=\"458\" src=\""+ json['bottomImage'] + "\"\>");
				console.log('bottom');
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
