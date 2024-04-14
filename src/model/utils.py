import model.config as cfg


def order_files_numerically(files_list, target_dir):
    numbers = list(range(1, len(files_list)+1))
    filenames = []
    for num in numbers:
        filenames.append(f"{target_dir}{num}.json")
    
    return filenames


def format_pokemon_types(pokemon_types, calculate_weaknesses, types_simple_format=False):
    formatted_types = []
    for type_info in pokemon_types:
        type_name = type_info if types_simple_format else type_info[0]
        target_type = cfg.types_dict[type_name]
        formatted_types.append([type_name, target_type[0], target_type[1]])

    if calculate_weaknesses:
        first_type_dict = pokemon_types[0][1]
        # list() function used to create a copy of the list and not only a reference
        weaknesses = list(first_type_dict["double_damage_from"])
        if len(pokemon_types) == 2:
            second_type_dict = pokemon_types[1][1]
            weaknesses = [item for item in weaknesses if item not in second_type_dict["half_damage_from"] and item not in second_type_dict["no_damage_from"]]
            for item in second_type_dict["double_damage_from"]:
                if item not in first_type_dict["half_damage_from"] and item not in first_type_dict["no_damage_from"]:
                    weaknesses.append(item)
            
        formatted_weaknesses = []
        for type_name in set(weaknesses):
            target_type = cfg.types_dict[type_name]
            multiplier = "x 4" if weaknesses.count(type_name) == 2 else "x 2"
            formatted_weaknesses.append([type_name, target_type[0], multiplier])

        return formatted_types, formatted_weaknesses
    
    return formatted_types


def get_type_translation(type_name):
    return cfg.types_dict[type_name][0]


def format_pokemon_weaknesses(pokemon_types):
    formatted_types = []
    for element in pokemon_types:
        target_type = cfg.types_dict[element]
        formatted_types.append([element, target_type[0], target_type[1]])

    return formatted_types


def format_pokemon_stats(pokemon_stats):
    formatted_stats = {}
    for stat_name, stat_value in pokemon_stats.items():
        target_stat = cfg.stats_dict[stat_name]
        formatted_stats[target_stat] = stat_value

    return formatted_stats
