/*$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');

    $("#mechanicform").submit(function(event){
        event.preventDefault();
        $.ajax({
             type:"POST",
             url:"/mechanic/update/",
             data: $("#mechanicform").serialize(),
    beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
             success: function(data){
                $("#mechanicform").trigger('reset');
                alert(data + " added successfully")
             },
             error: function(){
                alert("Something went wrong plz try again")
                window.location.href = "/home/"
             }
        });
        return false; //<---- move it here
   });
});
*/
