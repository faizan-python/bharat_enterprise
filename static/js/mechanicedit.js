$(document).ready(function() {
var csrftoken = getCookie('csrftoken');

       $("#mechaniceditform").submit(function(event){
            event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"",
                 data: $("#mechaniceditform").serialize(),
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
                 success: function(data){
                    window.location.href = "/mechanic/view/"
                 },
                 error: function(){
                    $.toast({
                        heading: 'Error',
                        text: 'Something went wrong!!! Please try again.',
                        icon: 'error',
                        hideAfter: 4000,
                        position: 'bottom-right'
                    })                 }
            });
            return false; //<---- move it here
       });
});
