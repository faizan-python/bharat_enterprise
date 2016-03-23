$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');

    $("#customerdropdown").change(function() {
        var service_id = $('#customerdropdown').val();
        id = parseInt(service_id)
        if (id > 0) {
            window.location.href = "/service/invoice/create/"+id+"/"
        }
    });

    $("#invoicedropdown").change(function() {
        var service_id = $('#invoicedropdown').val();
        id = parseInt(service_id)
        if (id > 0) {
            window.location.href = "/service/invoice/create/"+id+"/"
        }
    });
});
