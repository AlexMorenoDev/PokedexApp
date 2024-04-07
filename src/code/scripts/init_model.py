import os
import requests
import json
import utils as utils
import constants as const


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

        # Get pokemon description and evolution chain (evolution chain is saved to a json file)
        res_species = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/")
        if res_species.status_code == 200:
            pokemon_species = res_species.json()
            pokemon_info["desc"] = utils.get_translated_field(pokemon_species["flavor_text_entries"], "flavor_text", "es")
        else:
            print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon species - in get_pokemon_info()].\n{res_species.raise_for_status()}")
            return None

        return pokemon_info
    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon info].\n{res_pokemon_info.raise_for_status()}")
        return None
    

def download_pokemon_media(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    res_pokemon_info = requests.get(url)
    
    if res_pokemon_info.status_code == 200:
        pokemon_data = res_pokemon_info.json()

        # Download pokemon cry and images only if they dont exist
        utils.save_file_from_url(pokemon_data["cries"]["latest"], f"../../static/pokemon/cries/ogg/{pokemon_id}.ogg")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../../static/pokemon/images/normal/{pokemon_id}.png")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../../static/pokemon/images/shiny/{pokemon_id}.png" )

        # Download pokemon sprites only if they dont exist
        for path in const.pokemon_dirs:
            parts = path.split("/")
            if parts[4] == "sprites":
                sprite_type_selector = parts[7]
                if parts[8] == "male":
                    if parts[6] == "normal":
                        sprite_type_selector += "_default"
                    else:
                        sprite_type_selector += "_shiny"
                else:
                    if parts[6] == "normal":
                        sprite_type_selector += "_female"
                    else:
                        sprite_type_selector += "_shiny_female"

                sprite_url = None
                sprite_extension = None
                if parts[5] == "animated":
                    sprite_url = pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"][sprite_type_selector]
                    sprite_extension = ".gif"
                else:
                    sprite_url = pokemon_data["sprites"]["versions"]["generation-v"]["black-white"][sprite_type_selector]
                    sprite_extension = ".png"

                utils.save_file_from_url(sprite_url, path + str(pokemon_id) + sprite_extension)

    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon info].\n{res_pokemon_info.raise_for_status()}")
        return None


# TO DO: GUARGAR EN UN JSON APARTE LA EVOLUTION_CHAIN EN UNA CARPETA NUEVA Y CONECTARLO CON CADA POKEMON AÑADIENDO 
# UN CAMPO EVOLUTION_CHAIN_ID EN SU CORRESPONDIENTE JSON EN LA CARPETA INFO 

# Gets evolution chain info and return a formatted dictionary
def get_evolution_chain(pokemon_id, pokemon_info_json):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    res_pokemon_species = requests.get(url)

    if res_pokemon_species.status_code == 200:
        pokemon_species_data = res_pokemon_species.json()

        res_evolution_chain = requests.get(pokemon_species_data["evolution_chain"]["url"])
        if res_evolution_chain.status_code == 200:
            evolution_chain_data = res_evolution_chain.json()
            
            evolution_chain = {}
            evolution_chain_id = evolution_chain_data["id"]
            if not os.path.isfile(const.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"):
                start_pokemon = evolution_chain_data["chain"]
                start_pokemon_name = start_pokemon["species"]["name"]
                res_pokemon_info = requests.get("https://pokeapi.co/api/v2/pokemon/" + start_pokemon_name)
                pokemon_data = res_pokemon_info.json()
                evolution_chain["id"] = pokemon_data["id"]
                evolution_chain["name"] = start_pokemon_name
                evolution_chain["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                evolution_chain["evolves_to"] = []
                
                for evolution_1 in start_pokemon["evolves_to"]:
                    evolution_1_dict = {}
                    evolution_1_name = evolution_1["species"]["name"]
                    res_pokemon_info = requests.get("https://pokeapi.co/api/v2/pokemon/" + evolution_1_name)
                    pokemon_data = res_pokemon_info.json()
                    evolution_1_dict["id"] = pokemon_data["id"]
                    evolution_1_dict["name"] = evolution_1_name
                    evolution_1_dict["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                    evolution_1_dict["evolves_to"] = []
                    for evolution_2 in evolution_1["evolves_to"]:
                        evolution_2_dict = {}
                        evolution_2_name = evolution_2["species"]["name"]
                        res_pokemon_info = requests.get("https://pokeapi.co/api/v2/pokemon/" + evolution_2_name)
                        pokemon_data = res_pokemon_info.json()
                        evolution_2_dict["id"] = pokemon_data["id"]
                        evolution_2_dict["name"] = evolution_2_name
                        evolution_2_dict["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                        evolution_2_dict["evolves_to"] = []

                        evolution_1_dict["evolves_to"].append(evolution_2_dict)
                    
                    evolution_chain["evolves_to"].append(evolution_1_dict)

            with open(pokemon_info_json, "r") as json_file:
                pokemon_info = json.load(json_file)
            pokemon_info["evolution_chain_id"] = evolution_chain_id
            with open (pokemon_info_json, "w") as output_file: 
                json.dump(pokemon_info, output_file)
            print(f"INFO: Añadido campo 'evolution_chain_id' al archivo '{pokemon_info_json}'")

            return evolution_chain, evolution_chain_id
        else:
            print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon evolution chain].\n{res_evolution_chain.raise_for_status()}")
            return None

    else:
        print(f"ERROR: Hay un problema al conectarse con la Poke API [pokemon species].\n{res_evolution_chain.raise_for_status()}")
        return None


def main():
    utils.create_folders_structure(const.pokemon_dirs)

    if const.remove_pokemon_info:
        utils.remove_dir_files(const.pokemon_info_path)
    if const.remove_pokemon_evolution_chain:
        utils.remove_dir_files(const.pokemon_evolution_chains_path)

    for pokemon_id in range(const.pkm_id_start, const.pkm_id_end+1): 
        pokemon_info_json = const.pokemon_info_path + str(pokemon_id) + ".json"
        if not os.path.isfile(pokemon_info_json):
            pokemon_info = get_pokemon_info(pokemon_id)
            with open (pokemon_info_json, "w") as output_file: 
                json.dump(pokemon_info, output_file)
            print(f"INFO: Se ha guardado el archivo '{pokemon_info_json}' correctamente!")
        else:
            print(f"INFO: El archivo '{pokemon_info_json}' ya existe. Omitiendo...")

        download_pokemon_media(pokemon_id)

        pokemon_evolution_chain, evolution_chain_id = get_evolution_chain(pokemon_id, pokemon_info_json)
        if pokemon_evolution_chain:
            evolution_chain_json = const.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"
            with open (evolution_chain_json, "w") as output_file: 
                json.dump(pokemon_evolution_chain, output_file)
            print(f"INFO: Se ha guardado el archivo '{evolution_chain_json}' correctamente!")
        else:
            print(f"INFO: El archivo '{evolution_chain_json}' ya existe. Omitiendo...")


if __name__ == '__main__':
    main()