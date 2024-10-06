from flask import Flask, render_template, abort
import model.model as db
from math import ceil

app = Flask(__name__, template_folder="../templates", static_folder="../static")
db_path = "../static/pokemon/info/"
max_pages = 8
num_pokemon_per_page = 12


@app.route("/", methods=['GET'])
def pokedex_home():
    global db_path, max_pages

    type_names = db.get_types_names_and_colors()
    num_pages = ceil(db.get_all_pokemon_count(db_path) / num_pokemon_per_page)
    return render_template("pokemon_list.html", num_pages=num_pages, max_pages=max_pages, type_names=type_names)


@app.route("/<type_filter>", methods=['GET'])
def pokedex_home_filtered(type_filter):
    global db_path, max_pages

    type_names = db.get_types_names_and_colors()
    num_pages = ceil(db.get_filtered_pokemon_count(db_path, type_filter) / num_pokemon_per_page)
    return render_template("pokemon_list_filtered.html", num_pages=num_pages, max_pages=max_pages, type_filter=type_filter, type_names=type_names)


@app.route("/pokemon-names", methods=['GET'])
def get_pokemon_names():
    global db_path

    return {"pokemon_names": db.get_all_pokemon_names(db_path)}


@app.route("/pokemon-list/<page_id>", methods=['GET'])
def get_pokemon_list(page_id):
    global db_path, num_pokemon_per_page

    ending_id = int(page_id) * num_pokemon_per_page
    starting_id = ending_id - (num_pokemon_per_page - 1)
    return {"pokemon_list": db.get_pokemon_list(db_path, starting_id, ending_id)}


@app.route("/pokemon-list/filter/<type_filter>/<page_id>", methods=['GET'])
def get_filtered_pokemon_list(type_filter, page_id):
    global db_path, num_pokemon_per_page

    ending_id = int(page_id) * num_pokemon_per_page
    starting_id = ending_id - (num_pokemon_per_page - 1)
    
    return {"pokemon_list": db.get_filtered_pokemon_list(db_path, type_filter, starting_id, ending_id, num_pokemon_per_page)}
    


@app.route("/pokemon/<pokemon_id>", methods=['GET'])
def pokemon_info_detail(pokemon_id):
    global db_path

    pokemon_info = db.get_pokemon_detail(db_path + pokemon_id + ".json")
    if not pokemon_info:
        abort(404)
    pokemon_info["total_pokemon_count"] = db.get_all_pokemon_count(db_path)
    pokemon_types_names = db.get_types_names()
    return render_template("pokemon_detail.html", pokemon_info=pokemon_info, pokemon_types_names=pokemon_types_names)


@app.route("/tabla-tipos", methods=['GET'])
def types_chart():
    pokemon_types_chart, translated_types = db.get_pokemon_types_chart()
    return render_template("types_chart.html", pokemon_types_chart=pokemon_types_chart, translated_types=translated_types)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

app.register_error_handler(404, page_not_found)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
