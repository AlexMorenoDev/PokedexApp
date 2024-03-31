$(document).ready(function () {
    $(".card-subtitle").each(function() {
        var item_text = $(this).text();
        item_text = item_text.padStart(3, '0');
        $(this).text("N.º " + item_text);
    });
});