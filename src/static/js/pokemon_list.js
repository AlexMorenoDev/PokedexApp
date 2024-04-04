$(document).ready(function () {
    /* Format pokemon id */
    $(".card-subtitle").each(function() {
        var item_text = $(this).text();
        item_text = item_text.padStart(3, '0');
        $(this).text("N.º " + item_text);
    });

    /* 'Load more' button implementation */
    var num_items = $('.listing').length;
    var num_items_showing = 12;
    var increase_num = 12;
    var pokemon_cols = $('[id^=pokemon-col-]');
    $('#load-more-button').click(function () {
        if (num_items_showing <= num_items) {
            num_items_showing += increase_num;
        
            var load_end_index = null;
            if (num_items_showing <= num_items) {
                $('.listing:lt('+num_items_showing+')').show();
                load_end_index = num_items_showing;
            } else {
                $('.listing:lt('+num_items+')').show();
                load_end_index = num_items;
            }
            var target_images = pokemon_cols.slice(num_items_showing - increase_num, load_end_index);
            if (target_images != null) {
                target_images.each(function() {
                    var id = this.id.split('-')[2];
                    $('#pokemon-img-' + id).attr("src", "/static/pokemon/images/normal/" + id + ".png");
                });
            }
        }

        var load_more_button = $("#load-more-button");
        if (num_items_showing >= num_items) { 
            load_more_button.remove();
        } else {
            load_more_button.blur();
        }
        window.scrollTo(0, window.scrollY + 200);
    });
});