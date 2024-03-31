import os
import json
import model.utils as utils


def get_all_pokemon(target_dir):
    pokemon_list = []

    for filename in utils.order_files_numerically(os.listdir(target_dir), target_dir):
        if os.path.isfile(filename):
            pokemon_info = {}
            with open(filename, 'r') as json_file:
                pokemon_info_temp = json.load(json_file)
            pokemon_info["id"] = str(pokemon_info_temp.get("id"))
            pokemon_info["name"] = pokemon_info_temp.get("name").capitalize()
            pokemon_info["types"] = utils.format_pokemon_types(pokemon_info_temp.get("types"))
            pokemon_list.append(pokemon_info)
        else:
            pokemon_list.append(None)
    
    return pokemon_list


def get_pokemon_detail(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as json_file:
            pokemon_info = json.load(json_file)
        pokemon_info["id"] = str(pokemon_info.get("id"))
        pokemon_info["name"] = pokemon_info.get("name").capitalize()
        pokemon_info["types"] = utils.format_pokemon_types(pokemon_info.get("types"))
        return pokemon_info
    else:
        return None
