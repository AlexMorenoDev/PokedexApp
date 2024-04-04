import model.variables as vrs


def order_files_numerically(files_list, target_dir):
    numbers = list(range(1, len(files_list)+1))
    filenames = []
    for num in numbers:
        filenames.append(f"{target_dir}{num}.json")
    
    return filenames


def format_pokemon_name(pokemon_name):
    pokemon_name = pokemon_name.capitalize()
    if pokemon_name.endswith("-f"):
        return pokemon_name.replace("-f", " ♀")
    if pokemon_name.endswith('-m'):
        return pokemon_name.replace("-m", " ♂")
    
    return pokemon_name


def format_pokemon_types(pokemon_types):
    formatted_types = []
    for element in pokemon_types:
        target_type = vrs.types_dict[element]
        formatted_types.append([element, target_type[0], target_type[1]])

    return formatted_types


def format_pokemon_stats(pokemon_stats):
    formatted_stats = {}
    for stat_name, stat_value in pokemon_stats.items():
        target_stat = vrs.stats_dict[stat_name]
        formatted_stats[target_stat] = stat_value

    return formatted_stats
