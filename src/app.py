from flask import Flask, render_template, abort
import model.model as db

app = Flask(__name__, template_folder="../templates", static_folder="../static")
db_path = "../static/pokemon/info/"


@app.route("/")
def pokedex_home():
    global db_path

    pokemon_list = db.get_all_pokemon(db_path)
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/pokemon/<pokemon_id>")
def pokemon_info_detail(pokemon_id):
    global db_path

    pokemon_info = db.get_pokemon_detail(db_path + pokemon_id + ".json")
    if not pokemon_info:
        abort(404)
    pokemon_info["total_pokemon_count"] = db.get_all_pokemon_count(db_path)
    return render_template("pokemon_detail.html", pokemon_info=pokemon_info)


@app.route("/tabla-tipos")
def types_chart():
    pokemon_types_chart, translated_types = db.get_pokemon_types_chart()
    return render_template("types_chart.html", pokemon_types_chart=pokemon_types_chart, translated_types=translated_types)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

app.register_error_handler(404, page_not_found)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
