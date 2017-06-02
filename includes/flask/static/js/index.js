$(function(){
        $('#btnSignUp').click(function(){
                var btn = $(this);

                btn.prop('disabled',true);

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
                                btn.prop('disabled',false);

                        } else {
                        
                        $("#topImage").html("WARNING: " + _msg);
                                console.log('error');
                                btn.prop('disabled',false);
                        }
                        },
                        error: function(error){
                                console.log(error);
                                btn.prop('disabled',false);
                        }
                });

                //$.post(/*...*/).complete(function(){
                //      btn.prop('disabled',false);
                //});
        });
});
