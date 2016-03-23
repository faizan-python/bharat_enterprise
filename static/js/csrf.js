function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function numbersonly(myfield, e, dec) { 
    var key; var keychar; 
    if (window.event) key = window.event.keyCode; 
    else if (e) key = e.which; 
    else return true; 
    keychar = String.fromCharCode(key); 
// control keys
 if ((key==null) || (key==0) || (key==8) || (key==9) || (key==13) || (key==27) ) return true;
  // numbers
else if ((("0123456789.").indexOf(keychar) > -1)) return true; 
   // decimal point jump 
else if (dec && (keychar == ".")) { 
    myfield.form.elements[dec].focus(); 
    return false; } 
    else return false; 
}

function floatonly(myfield, e, dec) { 
    var key; var keychar; 
    if (window.event) key = window.event.keyCode; 
    else if (e) key = e.which; 
    else return true; 
    keychar = String.fromCharCode(key); 
// control keys
 if ((key==null) || (key==0) || (key==8) || (key==9) || (key==13) || (key==27) ) return true;
  // numbers
else if ((("0123456789.").indexOf(keychar) > -1)) return true; 
   // decimal point jump 
else if (dec && (keychar == ".")) { 
    myfield.form.elements[dec].focus(); 
    return false; } 
    else return false; 
}
