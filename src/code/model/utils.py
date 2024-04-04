
def order_files_numerically(files_list, target_dir):
    numbers = list(range(1, len(files_list)+1))
    filenames = []
    for num in numbers:
        filenames.append(f"{target_dir}{num}.json")
    
    return filenames


def format_pokemon_types(pokemon_types):
    # this dict contains type translation and type background color in hexadecimal format
    types_dict = {
        "normal": ["normal", "#f5f5f5"], "fire": ["fuego", "#fbd3d3"], "water": ["agua", "#bae4f0"],
        "electric": ["eléctrico", "#fff4d6"], "grass": ["planta", "#e0eed4"], "ice": ["hielo", "#dff8fb"],
        "fighting": ["lucha", "#eeb2af"], "poison": ["veneno", "#ffdeff"], "ground": ["tierra", "#efe6dc"],
        "flying": ["volador", "#d4e0f2"], "psychic": ["psíquico", "#ffc6d5"], "bug": ["bicho", "#d1d8c4"],
        "rock": ["roca", "#f1ebd2"], "ghost": ["fantasma", "#c7b1d5"], "dragon": ["dragón", "#d8c9fc"],
        "dark": ["siniestro", "#646464"], "steel": ["acero", "#ececec"], "fairy": ["hada", "#ffecf2"]
    }

    formatted_types = []
    for element in pokemon_types:
        target_type = types_dict[element]
        formatted_types.append([element, target_type[0], target_type[1]])

    return formatted_types


def format_pokemon_stats(pokemon_stats):
    stats_dict = {
        "hp": "PS", "attack": "Ataque", 
        "defense": "Defensa", "special-attack": "At. Esp.", 
        "special-defense": "Def. Esp.", "speed": "Velocidad",
        "total": "Total"
    }

    formatted_stats = {}
    for stat_name, stat_value in pokemon_stats.items():
        target_stat = stats_dict[stat_name]
        formatted_stats[target_stat] = stat_value

    return formatted_stats