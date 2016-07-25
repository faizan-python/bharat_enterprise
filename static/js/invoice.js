$(document).ready(function() {
    advance_pay_available = false
    $("#vendordropdown").prop("disabled", false);
    $("#vehicaldropdown").prop("disabled", false);

    var csrftoken = getCookie('csrftoken');
    $("#addvendor").click(function(event) {
      event.preventDefault();
      $("#vendorform").show();
      $("#vendorform").trigger('reset');
      $('#vendorform input').attr('readonly', false);
      $('#vendorform textarea').attr('readonly', false);
      $("#vendordropdown").prop("disabled", true);
      $("#vehicaldropdown").prop("disabled", true);
      deletevehicleoption()
      $("#vechicalform").show();
    });

    $("#addvehical").click(function(event) {
      event.preventDefault();
      $("#vehicaldropdown").prop("disabled", true);
      $("#vechicalform").trigger('reset');
      $("#vechicalform").show();
    });

    function autofillCustomerform(data) {
        $("#vendorform").autofill(data);
        $("#vendorform").show();
        $('#vendorform input').attr('readonly', 'readonly');
        $('#vendorform textarea').attr('readonly', 'readonly');
    }

    function deletevehicleoption() {
        $("#vehicaldropdown").find("option").each(function() {
          if ($(this).attr("id") != "default_vehicle_dropdown") {
                $(this).remove();
          }
        })
    }

    $("#vendordropdown").change(function() {
        var vendor_id = $('#vendordropdown').val();
        deletevehicleoption()
        $("#vechicalform").trigger('reset');
        $("#vechicalform").hide();
        $("#vehicaldropdown").val("default_vehicle_dropdown");
    
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
                vehicals = data['vehicle']
                advance_block = data['advance_block']
                $('#advance_amount_block').html(advance_block)

                if (vehicals) {
                    for (i = 0; i < vehicals.length; ++i) { 
                        $('#vehicaldropdown').append($('<option></option>').val(i).html(vehicals[i].vehicle_number));
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

    $('body').on('click', '#advance_pay_yes', function (event) {
      $("#vehicalcompleteform").show();
      advance_pay_deduct = true
      advance_pay_available = true
      $("input.group1").attr("disabled", true);
    });

    $('body').on('click', '#advance_pay_no', function (event) {
      advance_pay_deduct = false
      advance_pay_available = true
      $("input.group1").attr("disabled", true);
    });

    $("#vehicaldropdown").change(function() {
        if ($(this).val() != "default_vehicle_dropdown") {
            var vehical_id = $('#vehicaldropdown').val();
            $("#vechicalform").autofill(vehicals[vehical_id]);
            $("#vechicalform").show();
            $('#vechicalform input').attr('readonly', 'readonly');
            $('#vechicalform textarea').attr('readonly', 'readonly');
        }
    });

    function customerdata() {
        if ($('#vendordropdown').is(':disabled')){ 
              return $("#vendorform").serialize()
           }
        else {
              return $('#vendordropdown').val()
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

    function submitinvoiceform(data) {
        $.ajax({
             type:"POST",
             url:"/invoice/create/",
             dataType: 'json',
             data: JSON.stringify(data),
            beforeSend: function(xhr) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
             success: function(data){
                window.location.href = "/invoice/detail/"+data+"/";
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

    var table_id = 1
    /*Part add and Calculation Table*/
    $("#additem").click(function(event){
        var row1= '<th id='+table_id+' scope="row"> # </th>'
        var row2='<td><input type="text" name="item_name" id="item_name" class="form-control" required></td>'
        var row3='<td><input type="text" name="weight" id="weight" class="form-control" onKeyPress="return floatonly(this, event)"required></td>'
        var row4='<td><input type="text" name="price" id="price" class="form-control" onKeyPress="return floatonly(this, event)" required></td>'
        var row5='<td><button class="btn btn-sm btn-default deleteitem" type="button">Delete</button></td>'
        $('#itemtable > tbody:last-child').append('<tr>'+row1+row2+row3+row4+row5+'</tr>')
        table_id += 1
    });

    $("#itemtable").on("click", ".deleteitem", function(){
        $(this).parent().parent().remove();
        table_id -= 1
    });

    /*Calculate Amount of Total Cost*/
    function checkifblank(data) {
        if (data){
            return data
        }
        return 0
    }

    function calculateSum() {
        var tbl = $('#itemtable');
        var sum = 0;
        var item_list = []

        /*Part Table*/
        tbl.find('tr').each(function () {
            var quantity = 0
            var price = 0
            var sub_dict = {}
            $(this).find('#item_name').each(function () {
                if (this.value.length != 0) {
                    sub_dict[this.id] = this.value;
                }
            });
            $(this).find('#weight').each(function () {
                if (!isNaN(this.value) && this.value.length != 0) {
                    quantity = checkifblank(parseInt(this.value));
                    sub_dict[this.id] = this.value;
                }
            });
            $(this).find('#price').each(function () {
                if (!isNaN(this.value) && this.value.length != 0) {
                    price = checkifblank(parseFloat(this.value));
                    sub_dict[this.id] = this.value
                }
            });
            item_list.push(sub_dict)
            sum += quantity * price
            $(this).find('.total').val(sum.toFixed(2));
        });

        var tax = checkifblank(parseFloat($('#tax').val()))
        var paid = checkifblank(parseFloat($('#total_paid').val()))
        var tax_cost = (tax*sum)/100
        sum += tax_cost
        var advance_payment = checkifblank(parseFloat($('#advance_payment').val()))

        if (paid > sum){
            alert("Paid amount cannot be more than total cost")
            return
        }

        $('#totalcost').val(sum);

        if (paid){
            var pending = sum - paid
            $('#total_pending').val(pending);
        }
        else{
            var pending = sum - advance_payment
            $('#total_pending').val(pending)
        }

        return {item_list:item_list}
    }

    $("#calculateamount").click(function(event){
        calculateSum()
        $.toast({
            heading: 'Cost Generated',
            text: 'Total Cost is ' + $('#totalcost').val(),
            icon: 'info',
            hideAfter: 4000,
            position: 'bottom-right'
        })
    });

    /*Generate INvoice*/
    $("#save").click(function(event){
        event.preventDefault();
        $("#vendorform").show();
        $("#vehicleform").show();

        if ($('#advance_pay_type').length) {
            if (advance_pay_available == false) {
                  $.toast({
                      heading: 'Warning!!!',
                      text: 'Please select the Checkbox of Advance Pay!!! ',
                      icon: 'warning',
                      hideAfter: 4000,
                      position: 'mid-center'
                  })
                return
            }
        }

        if ($('#vendorform').valid() && $('#tabledata').valid() && $('#costform').valid()) {
            $('body').loading({stoppable: false}, 'start');
            var list = calculateSum()
            var item_list = list.item_list
            var data = {
                "vendor": $('#vendorform').serializeJSON(),
                "vehicle_form": $('#vechicalform').serializeJSON(),
                "invoice_deatils": $("#invoiceform").serializeJSON(),
                "company": $('#companydropdown').val(),

                'total_cost': checkifblank($('#totalcost').val()),
                'tax' : checkifblank($('#tax').val()),
                'total_paid' : checkifblank($('#total_paid').val()),
                'pending_cost' : checkifblank($('#total_pending').val()),
                'item_data': item_list
            }
            if (advance_pay_available == true) {
                data.push({'advance_pay_deduct': advance_pay_deduct})
            }
            submitinvoiceform(data);
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
