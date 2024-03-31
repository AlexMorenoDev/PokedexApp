import os
import json


def order_files_numerically(files_list, target_dir):
    numbers = list(range(1, len(files_list)+1))
    filenames = []
    for num in numbers:
        filenames.append(f"{target_dir}{num}.json")
    
    return filenames


def translate_pokemon_types(pokemon_types):
    types_dict = {
        'normal': 'normal', 'fire': 'fuego', 'water': 'agua',
        'electric': 'eléctrico', 'grass': 'planta', 'ice': 'hielo',
        'fighting': 'lucha', 'poison': 'veneno', 'ground': 'tierra',
        'flying': 'volador', 'psychic': 'psíquico', 'bug': 'bicho',
        'rock': 'roca', 'ghost': 'fantasma', 'dragon': 'dragón',
        'dark': 'siniestro', 'steel': 'acero', 'fairy': 'hada'
    }

    translated_types = []
    for element in pokemon_types:
        translated_types.append([element, types_dict[element]])

    return translated_types


def get_pokemon_info(target_dir):
    pokemon_list = []

    for filename in order_files_numerically(os.listdir(target_dir), target_dir):
        if os.path.isfile(filename):
            with open(filename) as json_file:
                pokemon_info = json.load(json_file)
                pokemon_info["id"] = str(pokemon_info.get("id"))
                pokemon_info["name"] = pokemon_info.get("name").capitalize()
                pokemon_info["types"] = translate_pokemon_types(pokemon_info.get("types"))
                pokemon_list.append(pokemon_info)
        else:
            pokemon_list.append(None)
    
    return pokemon_list