$(document).ready(function() {

    function checkifblank(data) {
        if (data){
            return data
        }
        return 0
    }

    $("#pendingamount").click(function(event){
        $('body').loading({stoppable: false}, 'start');
        totalcost = checkifblank(parseFloat($('#totalcost').val()))
        pendingpayment = checkifblank(parseFloat($('#pending_amount').val()))
        pending_cost = checkifblank(parseFloat($('#total_pending').val()))
        $('#total_pending').val(pending_cost - pendingpayment)
        data = {
            "pending_payment": pendingpayment,
            "invoice_id": $('#invoice-number').val()
        }
        $.ajax({
             type:"POST",
             url:"/invoice/pending/payment/",
             data: JSON.stringify(data),
            beforeSend: function(xhr) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                $('body').loading('stop');
                window.location.reload();
             },
             error: function(){
                $('body').loading('stop');
                $.toast({
                    heading: 'Error',
                    text: 'Something went wrong!!! Please try again',
                    icon: 'error',
                    hideAfter: 4000,
                    position: 'bottom-right'
                })
             }
        });
    });
});
