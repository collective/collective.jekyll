jQuery(function($) {
    function toggleDocumentMouseDown(event) {
        if (jQuery(event.target).parents('.menu').length)
            // target is part of the menu, so just return and do the default
            return true;

         $('.menu > dd').removeClass('activated');
    };
    jQuery(document).mousedown(toggleDocumentMouseDown);
    $('.menu .menuHandle').click(function() {
        $(this).parents('dl').first().children('dd').toggleClass('activated');
    });
    $('.symptom').click(function() {
        $(this).children('.symptomHelp').slideToggle();
    });
});
