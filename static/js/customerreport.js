$(document).ready(function() {
	var dateToday = new Date();
	var csrftoken = getCookie('csrftoken');

  function customerreportform(url) {
      var customer_id = $('#customerdropdown').val();
      $.ajax({
           type:"POST",
           url:url,
           data: {
              "customer_id": customer_id
           },

          beforeSend: function(xhr) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          },
           success: function(data){
            $("#reportresult").html(data);
            $("#generate-invoice").show();
            $.toast({
                heading: 'Success',
                text: 'Report generated Successfully!!! ',
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

    $("#generate-report").click(function(event) {
      event.preventDefault();
      var url = ""
      customerreportform(url);
    });

    $("#generate-invoice").click(function(event) {
        event.preventDefault();
        var customer_id = $('#customerdropdown').val();
        window.location = "/service/customer/report/generate/"+ customer_id +"/"
    });
});
