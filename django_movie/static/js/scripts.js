$(window).scroll(function() {
if ($(this).scrollTop() > 100) {
  if ($('#up').is(':hidden')) {
    $('#up').css({opacity: 0.5}).fadeIn('slow');
  }
} else { $('#up').stop(true, false).fadeOut('fast'); }
});
$('#up').click(function() {
  $('html, body').stop().animate({scrollTop: 0}, 1000);
});
