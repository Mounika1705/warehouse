$(function() {
    var path = location.pathname.split('/')[1];
    $('nav .active').removeClass('active').removeAttr('style');
    if (path) {
        $('nav a[href^="/' + path + '"]').addClass('active').css('border-bottom', '3px solid orange');
    } else {
        $('nav a[href="/"').addClass('active').css('border-bottom', '3px solid orange');
    }
});
