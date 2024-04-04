import os
import requests
import json
import utils as utils


def format_stats_data(stats):
    formatted_stats = {}
    for stat_data in stats:
        formatted_stats[stat_data["stat"]["name"]] = stat_data["base_stat"]

    formatted_stats["total"] = sum(formatted_stats.values())

    return formatted_stats


def format_abilities_data(abilities):
    formatted_abilities = []
    for element in abilities:
        res_ability = requests.get(element["ability"]["url"])
        if res_ability.status_code == 200:
            ability_data = res_ability.json()
            name = utils.get_translated_field(ability_data["names"], "name", "es")
            desc = utils.get_translated_field(ability_data["flavor_text_entries"], "flavor_text", "es")
            hidden_ability_text = ""
            if element["is_hidden"]:
                hidden_ability_text = "(oculta)"
            formatted_abilities.append([name, desc, hidden_ability_text])
        else:
            print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon ability].\n{res_ability.raise_for_status()}")

    return formatted_abilities


def get_pokemon_info(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    res_pokemon_info = requests.get(url)
    
    if res_pokemon_info.status_code == 200:
        pokemon_data = res_pokemon_info.json()

        # Get pokemon generic info
        pokemon_info = {
            "id": pokemon_id,
            "name": pokemon_data["name"], 
            "attributes": {
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"]
            },
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]],
            "stats": format_stats_data(pokemon_data["stats"]),
            "abilities": format_abilities_data(pokemon_data["abilities"])
        }

        # Download pokemon cry and sprites only if they dont exist
        utils.save_file_from_url(pokemon_data["cries"]["latest"], f"../../static/pokemon/cries/ogg/{pokemon_id}.ogg")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../../static/pokemon/images/normal/{pokemon_id}.png")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../../static/pokemon/images/shiny/{pokemon_id}.png" )

        # Get pokemon description
        res_species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/")
        if res_species.status_code == 200:
            pokemon_species = res_species.json()
            pokemon_info["desc"] = utils.get_translated_field(pokemon_species["flavor_text_entries"], "flavor_text", "es")
        else:
            print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon species].\n{res_species.raise_for_status()}")
            return None

        return pokemon_info
    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon info].\n{res_pokemon_info.raise_for_status()}")
        return None


def main():
    pkm_id_start = 1
    pkm_id_end = 151
    # If pokemon info JSON files must be generated again set it to true
    remove_pokemon_info = True

    utils.create_folders_structure([
        "../../static/pokemon/cries/ogg/", 
        "../../static/pokemon/images/normal/", 
        "../../static/pokemon/images/shiny/",
        "../../static/pokemon/info/"
        ]
    )

    if remove_pokemon_info:
        utils.remove_dir_files("../../static/pokemon/info/")

    for pokemon_id in range(pkm_id_start, pkm_id_end+1): 
        pokemon_info = get_pokemon_info(pokemon_id)
        with open (f"../../static/pokemon/info/{pokemon_id}.json", "w") as output_file: 
            json.dump(pokemon_info, output_file)
        print(f"INFO: Se ha guardado el archivo '{pokemon_id}.json' correctamente!")
        

if __name__ == '__main__':
    main()