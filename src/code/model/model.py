import os
import json
import model.utils as utils
import model.constants as consts


def get_all_pokemon_count(target_dir):
    count = 0
    for filename in os.listdir(target_dir):
        if filename.endswith(".json"):
            count += 1
    
    return count


def get_all_pokemon(target_dir):
    pokemon_list = []

    for filename in utils.order_files_numerically(os.listdir(target_dir), target_dir):
        if os.path.isfile(filename):
            pokemon_info = {}
            with open(filename, 'r') as json_file:
                pokemon_info_temp = json.load(json_file)
            pokemon_info["id"] = str(pokemon_info_temp.get("id"))
            pokemon_info["name"] = utils.format_pokemon_name(pokemon_info_temp.get("name"))
            pokemon_info["types"] = utils.format_pokemon_types(pokemon_info_temp.get("types"))
            pokemon_list.append(pokemon_info)
    
    return pokemon_list


def get_pokemon_detail(filepath):
    if not os.path.isfile(filepath):
        return None
    
    with open(filepath, 'r') as json_file:
        pokemon_info = json.load(json_file)
    pokemon_info["id"] = str(pokemon_info.get("id"))
    pokemon_info["name"] = utils.format_pokemon_name(pokemon_info.get("name"))
    pokemon_info["types"] = utils.format_pokemon_types(pokemon_info.get("types"))
    pokemon_info["attributes"]["height"] = [str(float(pokemon_info.get("attributes").get("height")) / 10), "m", "Altura"]
    pokemon_info["attributes"]["weight"] = [str(float(pokemon_info.get("attributes").get("weight")) / 10), "kg", "Peso"]
    pokemon_info["stats"] = utils.format_pokemon_stats(pokemon_info.get("stats"))
    pokemon_info["evolution_chain"] = get_pokemon_evolution_chain(pokemon_info["evolution_chain_id"])
    
    return pokemon_info
    

def get_pokemon_evolution_chain(evolution_chain_id):
    filepath = consts.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"
    if not os.path.isfile(filepath):
        return None
    
    with open(filepath, 'r') as json_file:
        pokemon_evolution_chain = json.load(json_file)
    pokemon_evolution_chain["name"] = utils.format_pokemon_name(pokemon_evolution_chain.get("name"))
    pokemon_evolution_chain["types"] = utils.format_pokemon_types(pokemon_evolution_chain.get("types"))

    for evolution_1 in pokemon_evolution_chain["evolves_to"]:
        evolution_1["name"] = utils.format_pokemon_name(evolution_1.get("name"))
        evolution_1["types"] = utils.format_pokemon_types(evolution_1.get("types"))
        for evolution_2 in evolution_1["evolves_to"]:
            evolution_2["name"] = utils.format_pokemon_name(evolution_2.get("name"))
            evolution_2["types"] = utils.format_pokemon_types(evolution_2.get("types"))

    return pokemon_evolution_chain

    