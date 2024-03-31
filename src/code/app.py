from flask import Flask, render_template
import model.model as db


app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route("/")
def pokedex_home():
    pokemon_list = db.get_all_pokemon("../static/pokemon/info/")
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/pokemon/<pokemon_id>")
def pokemon_info_detail(pokemon_id):
    pokemon_info = db.get_pokemon_detail("../static/pokemon/info/" + pokemon_id + ".json")
    return render_template("pokemon_detail.html", pokemon_info=pokemon_info)


if __name__ == '__main__':
    app.run(debug=True)