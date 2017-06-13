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

                        $("#topImage").html("<script\>\n function rollover(my_image) {\n my_image.src=\"/static/bottom.bmp\";\n }\n </script\>\n"+"<script\>\n function mouseaway(my_image) {\n my_image.src=\"/static/top.jpg\";\n }\n </script\>\n"+ "<img height=\"294\" width=\"458\" src=\""+ json['topImage']+ "\" onmouseover=\"rollover(this)\" onmouseout=\"mouseaway(this)\"  \>");
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

        });
});
