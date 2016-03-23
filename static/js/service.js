$(document).ready(function() {
    $("#customerdropdown").prop("disabled", false);
    $("#vehicaldropdown").prop("disabled", false);

    var csrftoken = getCookie('csrftoken');
    $("#addcustomer").click(function(event) {
      event.preventDefault();
      $("#customerform").show();
      $("#customerform").trigger('reset');
      $('#customerform input').attr('readonly', false);
      $('#customerform textarea').attr('readonly', false);
      $('#customerform input:radio').attr('disabled', false);
      $("#customerdropdown").prop("disabled", true);
      $("#vehicaldropdown").prop("disabled", true);
      $("#vechicalform").show();
    });

    $("#addvehical").click(function(event) {
      event.preventDefault();
      $("#vehicaldropdown").prop("disabled", true);
      $("#vechicalform").show();
    });

    var dateToday = new Date(); 
    $("#expected-date").datepicker({
        minDate: dateToday
    });

    $("#vehical_service").click(function(event) {
      $("#vehicalcompleteform").show();
      service_type = "vehical"
      $("input.group1").attr("disabled", true);
    });

    $("#other").click(function(event) {
      service_type = "other"
      $("#othercompleteform").show();
      $("input.group1").attr("disabled", true);
    });

    function autofillCustomerform(data) {
        $("#customerform").autofill(data);
        $("#customerform").show();
        $('#customerform input').attr('readonly', 'readonly');;
        $('#customerform textarea').attr('readonly', 'readonly');;
        $('#customerform input:radio').attr('disabled', true);
    }

    $("#customerdropdown").change(function() {
        var customer_id = $('#customerdropdown').val();
            
        $.ajax({
             type:"POST",
             url:"/vehical/user/get/",
             data: {
                "id": customer_id
             },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                autofillCustomerform(data['customer'][0]);
                vehicals = data['vehicals']

                if (vehicals) {
                    for (i = 0; i < vehicals.length; ++i) { 
                        $('#vehicaldropdown').append($('<option></option>').val(i).html(vehicals[i].vehical_number));
                    }
                }
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

    $("#vehicaldropdown").change(function() {
        var vehical_id = $('#vehicaldropdown').val();
        $("#vechicalform").autofill(vehicals[vehical_id]);
        $("#vechicalform").show();
        $('#vechicalform input').attr('readonly', 'readonly');
        $('#vechicalform textarea').attr('readonly', 'readonly');
    });

    function customerdata() {
        if ($('#customerdropdown').is(':disabled')){ 
              return $("#customerform").serialize()
           }
        else {
              return $('#customerdropdown').val()
           }
    }
    
    function vehicaldata() {
        if ($('#vehicaldropdown').is(':disabled')){ 
              return $("#vechicalform").serialize()
           }
        else {
              return vehicals[$('#vehicaldropdown').val()]
           }
    }
    
    (function( $ ){
        $.fn.serializeJSON=function() {
            var json = {};
            jQuery.map($(this).serializeArray(), function(n, i){
                json[n['name']] = n['value'];
            });
            return json;
        };
    })( jQuery );

    function submitserviceform(data) {
        $.ajax({
             type:"POST",
             url:"/service/create/",
             dataType: 'json',
             data: JSON.stringify(data),
            beforeSend: function(xhr) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                window.location.href = "/service/pending/"
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
    }

    $("#serviceform").submit(function(event){
        event.preventDefault();
        $("#customerform").show();
        $("#vechicalform").show();
        if (service_type == "vehical") {
          service_type_form = '#vechicalform';
        }
        if (service_type == "other") {
          service_type_form = '#otherform';
        }

        if ($('#customerform').valid() && $(service_type_form).valid()) {
            $('body').loading({stoppable: false}, 'start');
            var data = {
                "customer": $('#customerform').serializeJSON(),
                service_type_form: $(service_type_form).serializeJSON(),
                "service_deatils": $("#serviceform").serializeJSON(),
                "mechanic": $('#mechanicdropdown').val(),
                "gender": $('#customerform input:radio:checked').val(),
                "service_type":service_type
            }
            submitserviceform(data);
        }
        else{
                    $.toast({
              heading: 'Error',
              text: 'Please validate all the above fields!!! ',
              icon: 'error',
              hideAfter: 4000,
              position: 'bottom-right'
          })
        }
    });
});
