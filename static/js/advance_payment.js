$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');
    function autofillCustomerform(data) {
        $("#vendorform").autofill(data);
        $("#vendorform").show();
        $('#vendorform input').attr('readonly', 'readonly');
        $('#vendorform textarea').attr('readonly', 'readonly');
        $("#advance_amount_input").show();
        $("#advance_button").show();
    }

    $("#vendordropdown").change(function() {
        var vendor_id = $('#vendordropdown').val();
            
        $.ajax({
             type:"POST",
             url:"/vehicle/vendor/get/",
             data: {
                "id": vendor_id
             },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                autofillCustomerform(data['vendor'][0]);
                $.toast({
                    heading: 'Success',
                    text: data['vendor'][0]+' Selected for advance Payment',
                    icon: 'success',
                    hideAfter: 4000,
                    position: 'bottom-right'
                })
             },
             error: function(){
                $.toast({
                    heading: 'Error',
                    text: 'Something went wrong! Please try again',
                    icon: 'error',
                    hideAfter: 4000,
                    position: 'bottom-right'
                })
             }
        });
    });

    $("#pay_advance_amount").click(function() {
    	if ($("#advance_amount").val() <= 0) {
            $.toast({
                heading: 'Warning!!!',
                text: 'Payment Amount Should be Greater than 0',
                icon: 'warning',
                hideAfter: 4000,
                position: 'bottom-right'
            })
    		return
    	}
        var vendor_id = $('#vendordropdown').val();
            
        $.ajax({
             type:"POST",
             url:"/payment/advance/pay/",
             data: {
                "id": vendor_id,
                "advance_amount": $("#advance_amount").val() 
             },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                $.toast({
                    heading: 'Success',
                    text: data,
                    icon: 'success',
                    hideAfter: 4000,
                    position: 'bottom-right'
                })
             },
             error: function(){
                $.toast({
                    heading: 'Error',
                    text: 'Something went wrong! Please try again',
                    icon: 'error',
                    hideAfter: 4000,
                    position: 'bottom-right'
                })
             }
        });
    });
});
