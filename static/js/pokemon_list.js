$(document).ready(function () {
    $.ajax({
        url : '/pokemon-list/1',
        type : 'GET',
        dataType:'json',
        success : function(data) {      
            insert_list_in_div(data);
        },
        error : function(request, error) {
            console.log(JSON.stringify(error));
        }
    });
    var last_page_selected = 1;
    $("#button-page-" + last_page_selected).css({"backgroundColor": "#fce2ac"});

    $("[id^=button-page-]").click(function() {
        let current_id = this.id.split("-")[2];
        $.ajax({
            url : '/pokemon-list/' + current_id,
            type : 'GET',
            dataType:'json',
            success : function(data) {      
                insert_list_in_div(data);
            },
            error : function(request, error) {
                console.log(JSON.stringify(error));
            }
        });
        $("#button-page-" + current_id).css({"backgroundColor": "#fce2ac"});
        $("#button-page-" + last_page_selected).css({"backgroundColor": "white"});
        last_page_selected = current_id;
    }); 

    var pages_limit = $(".page-item.d-visible").length;
    var num_pages = parseInt($("#num-pages").text());
    var page_id_start = parseInt($(".d-visible.page-element").first().children().first().attr('id').split("-")[2]);
    var page_id_end = page_id_start + pages_limit;

    $("#previous-pages-button").click(function() {
        page_id_start -= pages_limit;
        page_id_end -= pages_limit;
        $(".page-item.page-element").each(function(i, obj) {
            i += 1 // Start at 1
            if(i >= page_id_start && i < page_id_end) { // 'page_id_end' not included, so only '<' needed
                obj.classList.remove("d-none");
                obj.classList.add("d-visible");
            } else if(obj.classList.contains("d-visible")) {
                obj.classList.remove("d-visible");
                obj.classList.add("d-none");
            }
        });
        if(page_id_start == 1) {
            $(this).prop("disabled", true);
        }
        if(page_id_end <= num_pages) {
            $("#next-pages-button").prop("disabled", false);
        }
    }); 

    $("#next-pages-button").click(function() {
        page_id_start += pages_limit;
        page_id_end += pages_limit;
        $("[id^=page-]").each(function(i, obj) {
            i += 1 // Start at 1
            if(i >= page_id_start && i < page_id_end) { // 'page_id_end' not included, so only '<' needed
                obj.classList.remove("d-none");
                obj.classList.add("d-visible");
            } else if(obj.classList.contains("d-visible")) {
                obj.classList.remove("d-visible");
                obj.classList.add("d-none");
            }
        });
        if(page_id_end > num_pages) {
            $(this).prop("disabled", true);
        }
        if(page_id_start != 1) {
            $("#previous-pages-button").prop("disabled", false);
        }
    });
});

function insert_list_in_div(data) {
    let html_code = "";
    let pokemon_list = data["pokemon_list"];
    if (pokemon_list.length > 0) {
        pokemon_list.forEach((pokemon) => {
            html_code += `
        <div id="pokemon-col-` + pokemon.id + `" class="col-lg-3 mb-3 align-items-stretch justify-content-center mb-5 listing">
                <div id="` + pokemon.name.toLowerCase() + `" class="card">
                    <a href="/pokemon/` + pokemon.id + `"><img src="/static/pokemon/images/normal/` + pokemon.id + `.png" id="pokemon-img-` + pokemon.id + `" class="card-img-top" style="background-color: ` + pokemon.types[0][2] + `;" alt="Imagen no encontrada"></a>
                    <div class="card-body">
                        <h6 class="card-subtitle text-body-secondary">` + pokemon.id + `</h6>
                        <div class="row">
                            <div class="col">
                                <h4 class="card-title">` + pokemon.name + `</h4> 
                            </div>
                            <div class="col-auto">
                                <a class="btn btn-dark btn-sm" href="/pokemon/` + pokemon.id + `"><i class="fa fa-plus"></i></a>
                            </div>
                        </div>
                    <div class="d-flex justify-content-start`;
            if (pokemon.types.length == 2) {
                html_code += ' gap-3">'
            } else {
                html_code += '">'
            }
            pokemon.types.forEach((type) => {
                html_code += '<p class="type type-' + type[0] + '">' + type[1] + '</p>'
            });
            html_code += '</div></div></div></div>'
        });
    } else {
        html_code += '<p class="h4 gy-4 text-center">No se han podido recuperar los datos de los Pokemon</p>'
    }
    $("#pokemon-list").html(html_code);

    /* Format pokemon id */
    $(".card-subtitle").each(function () {
        let item_text = $(this).text();
        item_text = item_text.padStart(3, '0');
        $(this).text("N.º " + item_text);
    });
}
