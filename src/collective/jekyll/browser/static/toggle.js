jQuery(function($) {
    function toggleDocumentMouseDown(event) {
        if (jQuery(event.target).parents('.symptoms').length)
            // target is part of the menu, so just return and do the default
            return true;

         $('.diagnosis > .symptoms').hide();
    };
    jQuery(document).mousedown(toggleDocumentMouseDown);
    $('.diagnosis > .status').click(function() {
        $(this).siblings().first().toggle();
    });
});
