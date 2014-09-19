/* Project specific Javascript goes here. */


setTimeout(function() {
    $('#candidate_thanks').fadeOut(1500);
}, 2500);

$('.main_content_form').submit(function() {
    $(this).find('#mainformsubmit')
        .attr('disabled', 'disabled')
        .val('Contacting Satellite...');

    setTimeout(function() {
        $('#mainformsubmit').removeAttr('disabled');
        $('#mainformsubmit').val('Submit');
    }, 10000);
});
