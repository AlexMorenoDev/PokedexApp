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
});