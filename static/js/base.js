$(document).ready(function() {
var csrftoken = getCookie('csrftoken');

    $(".deletemechanic").click(function(event){
        console.log( $(this).attr("id"));
        var id =  $(this).attr("id");
        $.ajax({
            type:"POST",
            url:"/mechanic/delete/",
            data: {
                "id": id
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(data){
                console.log(data)
                $("#mechanic-"+id).hide()
             },
            error: function(){
                alert("Something went wrong plz try again")
                window.location.href = "/home/"
             }
        });
    });
});
