from flask import Flask, render_template
import model.model as db


app = Flask(__name__, template_folder="../templates", static_folder="../static")
db_folder = "../static/pokemon/info/"


@app.route("/")
def pokedex_home():
    global db_folder

    pokemon_list = db.get_all_pokemon(db_folder)
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/pokemon/<pokemon_id>")
def pokemon_info_detail(pokemon_id):
    global db_folder

    pokemon_info = db.get_pokemon_detail(db_folder + pokemon_id + ".json")
    pokemon_info["total_pokemon_count"] = db.get_all_pokemon_count(db_folder)
    return render_template("pokemon_detail.html", pokemon_info=pokemon_info)


if __name__ == '__main__':
    app.run(debug=True)