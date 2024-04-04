import os
import requests
import json


def create_folders_structure(folder_list):
    for folder in folder_list:
        if not os.path.isdir(folder):
            os.makedirs(folder)
            

def save_file_from_url(url, output_file):
    if not os.path.isfile(output_file):
        res = requests.get(url)
        if res.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(res.content)
            print(f"INFO: Se ha descargado el archivo correctamente desde '{url}'")
        else:
            print(f"ERROR: Hay un problema al descargar la archivo del siguiente enlace:\n{url}")
    else:
        print("INFO: El archivo que se quiere descargar ya existe. Omitiendo...")


def format_stats_data(stats):
    formatted_stats = {}
    for stat_data in stats:
        formatted_stats[stat_data["stat"]["name"]] = stat_data["base_stat"]

    formatted_stats["total"] = sum(formatted_stats.values())

    return formatted_stats


def get_translated_field(target_list, target_field, lang):
    for entry in target_list:
        if entry["language"]["name"] == lang:
            return entry[target_field]
    return None


def format_ability_data(abilities):
    formatted_abilities = []
    for element in abilities:
        res_ability = requests.get(element["ability"]["url"])
        if res_ability.status_code == 200:
            ability_data = res_ability.json()
            name = get_translated_field(ability_data["names"], "name", "es")
            desc = get_translated_field(ability_data["flavor_text_entries"], "flavor_text", "es")
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
            "abilities": format_ability_data(pokemon_data["abilities"])
        }

        # Download pokemon cry and sprites only if they dont exist
        save_file_from_url(pokemon_data["cries"]["latest"], f"../../static/pokemon/cries/ogg/{pokemon_id}.ogg")
        save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../../static/pokemon/images/normal/{pokemon_id}.png")
        save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../../static/pokemon/images/shiny/{pokemon_id}.png" )

        # Get pokemon species description
        res_species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/")
        if res_species.status_code == 200:
            pokemon_species = res_species.json()
            for entry in pokemon_species["flavor_text_entries"]:
                if entry["language"]["name"] == "es":
                    pokemon_info["desc"] = entry["flavor_text"]
                    break
        else:
            print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon species].\n{res_species.raise_for_status()}")
            return None

        return pokemon_info
    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon info].\n{res_pokemon_info.raise_for_status()}")
        return None
    
def remove_dir_files(path):
    for filename in os.listdir(path):
        filepath = path + filename
        if os.path.isfile(filepath):
            os.remove(filepath)
            print("INFO: El archivo '" + filepath + "' se ha eliminado correctamente!")


def main():
    pkm_id_start = 1
    pkm_id_end = 151
    # If pokemon info JSON files must be generated again set it to true
    remove_pokemon_info = True

    create_folders_structure([
        "../../static/pokemon/cries/ogg/", 
        "../../static/pokemon/images/normal/", 
        "../../static/pokemon/images/shiny/",
        "../../static/pokemon/info/"
        ]
    )

    if remove_pokemon_info:
        remove_dir_files("../../static/pokemon/info/")

    for pokemon_id in range(pkm_id_start, pkm_id_end+1): 
        pokemon_info = get_pokemon_info(pokemon_id)
        with open (f"../../static/pokemon/info/{pokemon_id}.json", "w") as output_file: 
            json.dump(pokemon_info, output_file)
        print(f"INFO: Se ha guardado el archivo '{pokemon_id}.json' correctamente!")
        

if __name__ == '__main__':
    main()