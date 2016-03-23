$(document).ready(function() {
var csrftoken = getCookie('csrftoken');

       $("#login").submit(function(event){
            $.ajax({
                 type:"POST",
                 url:"/login/",
                 data: {
                        'username': $('#username').val(),
                        'password': $('#password').val() // from form
                        },
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
                 success: function(data){
                     if (data == "Success"){
                        $.toast({
                            heading: 'Successfully Logged In',
                            text: 'Welcome '+ $('#username').val(),
                            icon: 'success',
                            hideAfter: 4000,
                            position: 'mid-center'
                        })
                        window.location.href = "/home/"
                     }
                     else{
                        $.toast({
                            heading: 'Error',
                            text: 'Username and Password do not match',
                            icon: 'error',
                            hideAfter: 4000,
                            position: 'mid-center'
                        })
                    }  
                 }
            });
            return false; //<---- move it here
       });
});
