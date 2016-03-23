$(document).ready(function() {
	var dateToday = new Date();
	var csrftoken = getCookie('csrftoken');
    $("#till-date").datepicker({
        maxDate: dateToday
    });
    $("#from-date").datepicker({
        maxDate: dateToday
    });

    $("#generate-report").click(function(event) {
        event.preventDefault();

        if ($("#from-date").val() && $("#till-date").val()){
            $.ajax({
                 type:"POST",
                 url:"",
                 data: $("#report-form").serialize(),

                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                 success: function(data){
                 	$("#reportresult").html(data);
                    $("#generate-invoice").show();
                    $.toast({
                        heading: 'Success',
                        text: 'Report Generated Sucessfully!!!',
                        icon: 'success',
                        hideAfter: 4000,
                        position: 'bottom-right'
                    })
                 },
                 error: function(){
                    $.toast({
                        heading: 'Error',
                        text: 'Something went wrong!!! Please try again',
                        icon: 'error',
                        hideAfter: 4000,
                        position: 'bottom-right'
                    })
                 }
            });
        }
        else{
            $.toast({
                heading: 'Error',
                text: 'Please fill out the Date fields!!!',
                icon: 'error',
                hideAfter: 4000,
                position: 'bottom-right'
            })
        }
    });

    $("#generate-invoice").click(function(event) {
        if ($("#from-date").val() && $("#till-date").val()){
            $("#report-form").submit();
        }
        else{
            $.toast({
                heading: 'Error',
                text: 'Please fill out the Date fields!!!',
                icon: 'error',
                hideAfter: 4000,
                position: 'bottom-right'
            })            
        }
    });
});
