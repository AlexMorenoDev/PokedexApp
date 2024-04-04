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


def get_pokemon_info(pokemon_id, json_file_exists):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    res_pokemon_info = requests.get(url)
    
    if res_pokemon_info.status_code == 200:
        pokemon_data = res_pokemon_info.json()

        if not json_file_exists:
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

        # Download pokemon cry and images only if they dont exist
        utils.save_file_from_url(pokemon_data["cries"]["latest"], f"../../static/pokemon/cries/ogg/{pokemon_id}.ogg")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../../static/pokemon/images/normal/{pokemon_id}.png")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../../static/pokemon/images/shiny/{pokemon_id}.png" )

        # Download pokemon sprites if they dont exist
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"],
            f"../../static/pokemon/sprites/animated/normal/male/{pokemon_id}.gif"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_shiny"],
            f"../../static/pokemon/sprites/animated/shiny/male/{pokemon_id}.gif"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_female"],
            f"../../static/pokemon/sprites/animated/normal/female/{pokemon_id}.gif"
        )
        utils.save_file_from_url(
             pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_shiny_female"],
             f"../../static/pokemon/sprites/animated/shiny/female/{pokemon_id}.gif"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["front_default"],
            f"../../static/pokemon/sprites/no_animated/normal/male/{pokemon_id}.png"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["front_shiny"],
            f"../../static/pokemon/sprites/no_animated/shiny/male/{pokemon_id}.png"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["front_female"],
            f"../../static/pokemon/sprites/no_animated/normal/female/{pokemon_id}.png"
        )
        utils.save_file_from_url(
            pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["front_shiny_female"],
            f"../../static/pokemon/sprites/no_animated/shiny/female/{pokemon_id}.png"
        )
        
        if not json_file_exists:
            # Get pokemon description
            res_species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/")
            if res_species.status_code == 200:
                pokemon_species = res_species.json()
                pokemon_info["desc"] = utils.get_translated_field(pokemon_species["flavor_text_entries"], "flavor_text", "es")
            else:
                print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon species].\n{res_species.raise_for_status()}")
                return None

            return pokemon_info
        return None
    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon info].\n{res_pokemon_info.raise_for_status()}")
        return None


def main():
    pkm_id_start = 1
    pkm_id_end = 151
    # If pokemon info JSON files must be generated again set it to true
    remove_pokemon_info = False

    utils.create_folders_structure([
        "../../static/pokemon/info/",
        "../../static/pokemon/cries/ogg/", 
        "../../static/pokemon/images/normal/", 
        "../../static/pokemon/images/shiny/",
        "../../static/pokemon/sprites/no_animated/normal/male/",
        "../../static/pokemon/sprites/no_animated/normal/female/",
        "../../static/pokemon/sprites/no_animated/shiny/male/",
        "../../static/pokemon/sprites/no_animated/shiny/female/",
        "../../static/pokemon/sprites/animated/normal/male/",
        "../../static/pokemon/sprites/animated/normal/female/",
        "../../static/pokemon/sprites/animated/shiny/male/",
        "../../static/pokemon/sprites/animated/shiny/female/"
        ]
    )

    pokemon_info_folder = "../../static/pokemon/info/"
    if remove_pokemon_info:
        utils.remove_dir_files(pokemon_info_folder)

    for pokemon_id in range(pkm_id_start, pkm_id_end+1): 
        json_filepath = pokemon_info_folder + str(pokemon_id) + ".json"
        json_file_exists = os.path.isfile(json_filepath)
        pokemon_info = get_pokemon_info(pokemon_id, json_file_exists)
        if not json_file_exists:
            with open (json_filepath, "w") as output_file: 
                json.dump(pokemon_info, output_file)
            print(f"INFO: Se ha guardado el archivo '{pokemon_id}.json' correctamente!")
        else:
            print(f"INFO: El archivo '{pokemon_id}.json' ya existe. Omitiendo...")
        

if __name__ == '__main__':
    main()