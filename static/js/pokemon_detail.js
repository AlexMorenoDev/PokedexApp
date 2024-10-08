$(document).ready(function () {
    /* Format pokemon id */
    $(".card-subtitle").each(function () {
        let item_text = $(this).text();
        item_text = item_text.padStart(3, '0');
        $(this).text("N.º " + item_text);
    });

    /* Set audio element volume */
    let audio = document.getElementById("pokemon-cry");
    audio.volume = 0.25;

    /* Swap pokemon image */
    $("#toggle-pokemon-image-button").click(function () {
        update_image_src("#pokemon-image", 4, "normal", "shiny");
    });

    /* Swap pokemon sprites */
    $("#toggle-pokemon-sprites-button").click(function () {
        update_image_src(".pokemon-sprite", 5, "normal", "shiny");
    });

    /* Rotate pokemon sprites */
    $("#rotate-pokemon-sprites-button").click(function () {
        update_image_src(".pokemon-sprite", 6, "front", "back");
    });

    /* Swap pokemon evolution chain images */
    $("#toggle-pokemon-evolution-chain-images-button").click(function () {
        update_image_src(".evolution-chain-img", 4, "normal", "shiny");
    });

    /* Set progress bar background color */
    $(".progress-bar").each(function() {
        current_bar = $(this);
        bar_value = current_bar.attr("aria-valuenow");

        color = null;
        switch (true) {
            case (bar_value > 0 && bar_value <= 30):
                color = "#db0e0e";
                break;
            case (bar_value > 30 && bar_value <= 50):
                color = "#ff7801";
                break;
            case (bar_value > 50 && bar_value <= 70):
                color = "#ffd635";
                break;
            case (bar_value > 70 && bar_value <= 110):
                color = "#98da14";
                break;
            case (bar_value > 110 && bar_value <= 150):
                color = "#23cd5e";
                break;
            case (bar_value > 150 && bar_value <= 180):
                color = "#3ab0c3";
                break;
            default:
                color = "#a818f2";
        }
        current_bar.css("background-color", color);
        
    });

    /* Initialize tooltip */
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
});

function update_image_src(selector, url_split_index, val_1, val_2) {
    $(selector).each(function () {
        let current_url = $(this).attr("src");
        if (current_url.split("/")[url_split_index] === val_1) {
            $(this).attr("src", current_url.replace(val_1, val_2))
        } else {
            $(this).attr("src", current_url.replace(val_2, val_1))
        }
    });
}