import os
import json
import model.utils as utils
import model.config as cfg


def get_all_pokemon_names(target_dir):
    pokemon_names = {}
    for filename in utils.order_files_numerically(os.listdir(target_dir), target_dir):
        if filename.endswith(".json"):
            with open(filename, 'r') as json_file:
                pokemon_info = json.load(json_file)
            pokemon_names[pokemon_info["id"]] = pokemon_info["name"]

    return pokemon_names


def get_all_pokemon_count(target_dir):
    count = 0
    for filename in os.listdir(target_dir):
        if filename.endswith(".json"):
            count += 1
    
    return count


def get_filtered_pokemon_count(target_dir, type_filter):
    count = 0
    for filename in os.listdir(target_dir):
        if filename.endswith(".json"):
            filepath = target_dir + filename
            with open(filepath, 'r') as json_file:
                pokemon_info = json.load(json_file)
            
            if utils.pokemon_type_match(pokemon_info.get("types"), type_filter):
                count += 1
    
    return count


def get_pokemon_list(target_dir, starting_id, ending_id):
    pokemon_list = []
    for i in range(starting_id, ending_id+1):
        filename = target_dir + str(i) + ".json"
        if os.path.isfile(filename):
            formatted_info = {}
            with open(filename, 'r') as json_file:
                pokemon_info = json.load(json_file)
            formatted_info["id"] = str(pokemon_info.get("id"))
            formatted_info["name"] = pokemon_info.get("name")
            formatted_info["types"] = utils.format_pokemon_types(pokemon_info.get("types"), calculate_weaknesses=False)
            pokemon_list.append(formatted_info)
    
    return pokemon_list


def get_filtered_pokemon_list(target_dir, type_filter, starting_id, ending_id, num_pokemon_per_page):
    filtered_pokemon_list = []
    i, j, num_pokemon_type = 1, 1, 1

    max_limit = get_all_pokemon_count(target_dir)
    while j <= num_pokemon_per_page:
        filename = target_dir + str(i) + ".json"
        if os.path.isfile(filename):
            with open(filename, 'r') as json_file:
                pokemon_info = json.load(json_file)

            pokemon_types = pokemon_info.get("types")
            if utils.pokemon_type_match(pokemon_types, type_filter):
                if num_pokemon_type >= starting_id and num_pokemon_type <= ending_id:
                    formatted_info = {}
                    formatted_info["id"] = str(pokemon_info.get("id"))
                    formatted_info["name"] = pokemon_info.get("name")
                    formatted_info["types"] = utils.format_pokemon_types(pokemon_types, calculate_weaknesses=False)
                    filtered_pokemon_list.append(formatted_info)
                    j += 1
                num_pokemon_type += 1
        if i > max_limit:
            break
        i += 1
    
    return filtered_pokemon_list


def get_pokemon_detail(filepath):
    if not os.path.isfile(filepath):
        return None
    
    with open(filepath, 'r') as json_file:
        pokemon_info = json.load(json_file)
    pokemon_info["id"] = str(pokemon_info.get("id"))
    pokemon_info["types"], pokemon_info["weaknesses"] = utils.format_pokemon_types(pokemon_info.get("types"), calculate_weaknesses=True)
    pokemon_info["attributes"]["height"] = [str(float(pokemon_info.get("attributes").get("height")) / 10), "m", "Altura"]
    pokemon_info["attributes"]["weight"] = [str(float(pokemon_info.get("attributes").get("weight")) / 10), "kg", "Peso"]
    pokemon_info["stats"] = utils.format_pokemon_stats(pokemon_info.get("stats"))
    pokemon_info["evolution_chain"] = get_pokemon_evolution_chain(pokemon_info["evolution_chain_id"])
    
    return pokemon_info
    

def get_pokemon_evolution_chain(evolution_chain_id):
    filepath = cfg.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"
    if not os.path.isfile(filepath):
        return None
    
    with open(filepath, 'r') as json_file:
        pokemon_evolution_chain = json.load(json_file)
    pokemon_evolution_chain["id"] = str(pokemon_evolution_chain.get("id"))
    pokemon_evolution_chain["types"] = utils.format_pokemon_types(pokemon_evolution_chain.get("types"), calculate_weaknesses=False, types_simple_format=True)

    for evolution_1 in pokemon_evolution_chain["evolves_to"]:
        evolution_1["id"] = str(evolution_1.get("id"))
        evolution_1["types"] = utils.format_pokemon_types(evolution_1.get("types"), calculate_weaknesses=False, types_simple_format=True)
        for evolution_2 in evolution_1["evolves_to"]:
            evolution_2["id"] = str(evolution_2.get("id"))
            evolution_2["types"] = utils.format_pokemon_types(evolution_2.get("types"), calculate_weaknesses=False, types_simple_format=True)

    return pokemon_evolution_chain


def get_types_names_and_colors():
    types_names_and_colors = []
    for type_info in cfg.types_dict.values():
        types_names_and_colors.append([type_info[0].capitalize(), type_info[1]])
    
    return types_names_and_colors


def get_types_names():
    types_names = []
    for type_info in cfg.types_dict.values():
        types_names.append(type_info[0].capitalize())
    
    return types_names


def get_pokemon_types_chart():
    with open(cfg.pokemon_types_chart_filepath, 'r') as json_file:
        types_chart = json.load(json_file)
    
    translated_types = []
    for type_name in types_chart:
        translated_types.append(utils.get_type_translation(type_name))

    return types_chart, translated_types
    
