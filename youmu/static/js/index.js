$( document ).ready(function() {
    $.stellar();
	$("#query").val($("#query_str").val());
});

$(window).load(function() {
    var navpos = $('.navbar').offset();
    $(window).bind('resize', function() {
        navpos = $('.navbar').offset();
    });

    $(window).bind('scroll', function() {
        if ($(window).scrollTop() > navpos.top) {
            $('.navbar').addClass('navbar-fixed');
            $('.masthead').addClass('masthead-expanded');
        }
        else {
            $('.navbar').removeClass('navbar-fixed');
            $('.masthead').removeClass('masthead-expanded');
        }
    }); 
});
