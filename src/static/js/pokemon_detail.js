$(document).ready(function () {
    $(".card-subtitle").each(function () {
        var item_text = $(this).text();
        item_text = item_text.padStart(3, '0');
        $(this).text("N.º " + item_text);
    });

    var audio = document.getElementById("pokemon-cry");
    audio.volume = 0.3;

    $("#toggle-pokemon-image-button").click(function () {
        var pokemon_image = $("#pokemon-image");
        var current_url = pokemon_image.attr("src");
        if (current_url.split("/")[4] === "normal") {
            pokemon_image.attr("src", current_url.replace("normal", "shiny"))
        } else {
            pokemon_image.attr("src", current_url.replace("shiny", "normal"))
        }
    });

    $(".progress-bar").each(function() {
        current_bar = $(this);
        bar_value = current_bar.attr("aria-valuenow");

        color = null;
        if (bar_value > 0 && bar_value <= 30) {
            color = "#db0e0e";
        } else if (bar_value > 30 && bar_value <= 50) {
            color = "#ff7801";
        } else if (bar_value > 50 && bar_value <= 70) {
            color = "#ffd635";
        } else if (bar_value > 70 && bar_value <= 110) {
            color = "#98da14";
        } else if (bar_value > 110 && bar_value <= 150) {
            color = "#23cd5e";
        } else if (bar_value > 150 && bar_value <= 180) {
            color = "#3ab0c3";
        } else {
            color = "#a818f2";
        }
        current_bar.css("background-color", color);
        
    });
});