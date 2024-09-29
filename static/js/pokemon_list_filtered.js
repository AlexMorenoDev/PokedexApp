$(document).ready(function () {
    var session_type_filter = sessionStorage.getItem("type_filter");
    var current_type_filter = $('#type-filter').text()
    if (!session_type_filter || session_type_filter != current_type_filter) {
        session_type_filter = current_type_filter;
        sessionStorage.setItem("type_filter", session_type_filter);
        sessionStorage.removeItem("reloading");
    }
    var pages_limit = $(".page-item.d-visible").length;
    var num_pages = parseInt($("#num-pages").text());
    var loading_spinners = $("#loading-spinners");
    var page_id_start = null;
    var last_page_selected_id = null;
    
    var reloading = sessionStorage.getItem("reloading");
    if (reloading) {
        last_page_selected_id = parseInt(sessionStorage.getItem("last_page_selected"));
        page_id_start = parseInt(sessionStorage.getItem("page_start"));
    } else {
        last_page_selected_id = 1;
        page_id_start = parseInt($(".d-visible.page-element").first().children().first().attr('id').split("-")[2]);

        loading_spinners.show();
        $.ajax({
            url: '/pokemon-list/filter/' + session_type_filter + "/" + last_page_selected_id,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                insert_list_in_div(data);
                loading_spinners.hide();
            },
            error: function (xhr, status, error) {
                $("#pokemon-list-ajax-alert").html(xhr.status + " - " + error + " <button class='btn btn-dark btn-sm' onClick='window.location.reload();'><i class='fa fa-refresh' aria-hidden='true'></i></button>");
                $("#pokemon-list-ajax-alert-div").show();
                loading_spinners.hide();
            }
        });

        $("#button-page-" + last_page_selected_id).prop("disabled", true);
    }

    if (last_page_selected_id == 1) {
        $("#previous-pages-button").prop("disabled", true);
    }

    var page_id_end = page_id_start + pages_limit;
 
    $("#button-page-" + last_page_selected_id).addClass("page-link-selected");
    $("[id^=button-page-]").click(function () {
        let current_id = this.id.split("-")[2];

        $('#pokemon-list').empty();
        loading_spinners.show();
        $.ajax({
            url: '/pokemon-list/filter/' + session_type_filter + '/' + current_id,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                insert_list_in_div(data);
                loading_spinners.hide();
            },
            error: function (xhr, status, error) {
                $("#pokemon-list-ajax-alert").html(xhr.status + " - " + error + " <button class='btn btn-dark btn-sm' onClick='reload_page(" + current_id + ", " + page_id_start + ");'><i class='fa fa-refresh' aria-hidden='true'></i></button>");
                $("#pokemon-list-ajax-alert-div").show();
                loading_spinners.hide();
            }
        });
        $("#button-page-" + current_id).addClass("page-link-selected");
        $("#button-page-" + current_id).prop("disabled", true);
        if (current_id != last_page_selected_id) {
            $("#button-page-" + last_page_selected_id).removeClass("page-link-selected");
            $("#button-page-" + last_page_selected_id).prop("disabled", false);
            last_page_selected_id = current_id;
            set_session_storage_values(last_page_selected_id, page_id_start);
        }
    });

    if (reloading) {
        if (page_id_start == 1) {
            $("#previous-pages-button").prop("disabled", true);
        }
        if (page_id_end > num_pages) {
            $("#next-pages-button").prop("disabled", true);
        }
        render_page_buttons(page_id_start, page_id_end);
        $("#button-page-" + last_page_selected_id).click();
    }

    $("#previous-pages-button").click(function () {
        page_id_start -= pages_limit;
        page_id_end -= pages_limit;
        render_page_buttons(page_id_start, page_id_end);
        if (page_id_start == 1) {
            $(this).prop("disabled", true);
        }
        if (page_id_end <= num_pages) {
            $("#next-pages-button").prop("disabled", false);
        }
    });

    $("#next-pages-button").click(function () {
        page_id_start += pages_limit;
        page_id_end += pages_limit;
        render_page_buttons(page_id_start, page_id_end);
        if (page_id_end > num_pages) {
            $(this).prop("disabled", true);
        }
        if (page_id_start != 1) {
            $("#previous-pages-button").prop("disabled", false);
        }
    });

    $('[id^=type-filter-button-]').each(function(i, obj) {
        const parts = obj.id.split("-")
        let type_filter = parts[3];
        let hex_color = parts[4];
        obj.style.setProperty('--dropdown-element-background-color', hex_color);
        
        $(this).on("click", function() {
            window.location.href = "/" + type_filter.toLowerCase();
        });
    });

    $("#remove-filter-button").click(function () {
        sessionStorage.removeItem("type_filter");
        sessionStorage.setItem("page_start", 1);
        sessionStorage.setItem("last_page_selected", 1);
        window.location.href = "/";
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

function render_page_buttons(start_id, end_id) {
    $("[id^=page-]").each(function (i, obj) {
        i += 1 // Start at 1
        if (i >= start_id && i < end_id) { // 'page_id_end' not included, so only '<' needed
            obj.classList.remove("d-none");
            obj.classList.add("d-visible");
        } else if (obj.classList.contains("d-visible")) {
            obj.classList.remove("d-visible");
            obj.classList.add("d-none");
        }
    });
}

function reload_page(button_id, page_id_start) {
    set_session_storage_values(button_id, page_id_start);
    window.location.reload();
}

function set_session_storage_values(button_id = null, page_id_start = null) {
    sessionStorage.setItem("reloading", "true");
    if (button_id)
        sessionStorage.setItem("last_page_selected", button_id);
    if (page_id_start)
        sessionStorage.setItem("page_start", page_id_start);
}
