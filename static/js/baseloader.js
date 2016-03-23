$(document).ready(function() {
  $('body').loading({stoppable: false}, 'start');
});

$(window).load(function() {
  $('body').loading('stop');
});
