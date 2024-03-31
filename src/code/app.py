from flask import Flask, render_template, send_from_directory
from utils.model import get_pokemon_info


app = Flask(__name__, template_folder="../templates", static_folder="../static")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory("../static/", "favicon.ico", mimetype='image/vnd.microsoft.icon')


@app.route("/")
def pokedex_home():
    pokemon_list = get_pokemon_info("../static/pokemon/info/")
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


if __name__ == '__main__':
    app.run(debug=True)