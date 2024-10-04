import os
import json
import utils
import config as cfg


def format_stats_data(stats):
    formatted_stats = {}
    for stat_data in stats:
        formatted_stats[stat_data["stat"]["name"]] = stat_data["base_stat"]

    formatted_stats["total"] = sum(formatted_stats.values())

    return formatted_stats


def format_abilities_data(abilities):
    formatted_abilities = []
    for element in abilities:
        ability_data = utils.make_pokeapi_call(
            element["ability"]["url"], 
            "pokemon ability - format_abilities_data()"
        )
        if ability_data:
            name = utils.get_translated_field(ability_data["names"], "name", "es")
            desc = utils.get_translated_field(ability_data["flavor_text_entries"], "flavor_text", "es")
            hidden_ability_text = ""
            if element["is_hidden"]:
                hidden_ability_text = "(oculta)"
            formatted_abilities.append([name, desc, hidden_ability_text])

    return formatted_abilities


def get_pokemon_info(pokemon_id):
    pokemon_info = None
    pokemon_data = utils.make_pokeapi_call(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", 
        "pokemon info - get_pokemon_info()"
    )
    if pokemon_data:
        # Get pokemon generic info
        pokemon_info = {
            "id": pokemon_id,
            "name": None, # Initialized later. I define it here to keep the order
            "attributes": {
                "height": pokemon_data["height"],
                "weight": pokemon_data["weight"]
            },
            "types": [],
            "stats": format_stats_data(pokemon_data["stats"]),
            "abilities": format_abilities_data(pokemon_data["abilities"])
        }

        # Get pokemon description and evolution chain (evolution chain is saved to a json file)
        pokemon_species_data = utils.make_pokeapi_call(
            f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/", 
            "pokemon species - get_pokemon_info()"
        )
        if pokemon_species_data:
            pokemon_info["name"] = utils.get_translated_field(pokemon_species_data["names"], "name", "es")
            pokemon_info["desc"] = utils.get_translated_field(pokemon_species_data["flavor_text_entries"], "flavor_text", "es")
        else:
            pokemon_info["name"], pokemon_info["desc"] = None, None

        # Get pokemon types and weaknesses
        for current_type in pokemon_data["types"]:
            type_data = utils.make_pokeapi_call(
                current_type["type"]["url"], 
                "pokemon type - get_pokemon_info()"
            )
            type_info = [
                current_type["type"]["name"], {
                    "double_damage_from": [element["name"] for element in type_data["damage_relations"]["double_damage_from"]],
                    "half_damage_from": [element["name"] for element in type_data["damage_relations"]["half_damage_from"]],
                    "no_damage_from": [element["name"] for element in type_data["damage_relations"]["no_damage_from"]]
                }
            ]

            pokemon_info["types"].append(type_info)

    return pokemon_info
    

def download_pokemon_media(pokemon_id):
    pokemon_data = utils.make_pokeapi_call(
        f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", 
        "pokemon info - download_pokemon_media()"
    )

    if pokemon_data:
        # Download pokemon cry and images only if they dont exist
        utils.save_file_from_url(pokemon_data["cries"]["latest"], f"../../static/pokemon/cries/ogg/{pokemon_id}.ogg")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../../static/pokemon/images/normal/{pokemon_id}.png")
        utils.save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../../static/pokemon/images/shiny/{pokemon_id}.png" )

        # Download pokemon sprites only if they dont exist
        for path in cfg.pokemon_dirs:
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


def get_evolution_details(evolution_details):
    formatted_evolution_details = []

    for evolution_data in evolution_details:
        new_dict = {}
        for key, value in evolution_data.items():
            if value:
                if key == "gender":
                    new_dict[key] = "female" if value == 1 else "male"
                elif key == "held_item" or key == "item":
                    object_info = utils.make_pokeapi_call(value["url"], "object info - get_evolution_details()")
                    object_dict = {}
                    object_dict["id"] = object_info["id"]
                    object_dict["name"] = utils.get_translated_field(object_info["names"], "name", "es")
                    utils.save_file_from_url(object_info["sprites"]["default"],  cfg.objects_dir + str(object_dict["id"]) + ".png")   
                    new_dict[key] = object_dict
                elif key == "known_move" or key == "known_move_type" or key == "party_type":
                    target_info = utils.make_pokeapi_call(value["url"], "object info - get_evolution_details()")
                    new_dict[key] = utils.get_translated_field(target_info["names"], "name", "es")
                elif key == "location":
                    new_dict[key] = value["name"].replace('-', ' ').capitalize() # This is formatted because it wont be translated
                elif key == "party_species" or key == "trade_species":
                    pokemon_info = utils.make_pokeapi_call(value["url"], "object info - get_evolution_details()")
                    new_dict[key] = pokemon_info["id"]
                elif  key == "relative_physical_stats":
                    options = {1 : "atk>def", 0: "atk=def", -1: "atk<def"}
                    new_dict[key] = options[value]
                elif key == "trigger":
                    new_dict[key] = cfg.trigger_translations.get(value["name"])
                else:
                    new_dict[key] = value   
                        
        formatted_evolution_details.append(new_dict)

    return formatted_evolution_details


# Gets evolution chain info and return a formatted dictionary
def get_evolution_chain(pokemon_id, pokemon_info_json):
    evolution_chain = {}
    evolution_chain_id = None
    
    pokemon_species_data = utils.make_pokeapi_call(
        f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}", 
        "pokemon species - get_evolution_chain()"
    )

    if pokemon_species_data:
        evolution_chain_data = utils.make_pokeapi_call(
            pokemon_species_data["evolution_chain"]["url"], 
            "evolution chain - get_evolution_chain()"
        )

        if evolution_chain_data:
            evolution_chain_id = evolution_chain_data["id"]
            if not os.path.isfile(cfg.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"):
                start_pokemon = evolution_chain_data["chain"]
                pokemon_species_url = start_pokemon["species"]["url"]
                pokemon_data = utils.make_pokeapi_call(
                    "https://pokeapi.co/api/v2/pokemon/" + pokemon_species_url.split("/")[6], 
                    "pokemon info - get_evolution_chain() - 0"
                )
                if pokemon_data:
                    pokemon_species_data = utils.make_pokeapi_call(pokemon_species_url, "pokemon species - get_evolution_chain() - 0")
                    if pokemon_species_data:
                        evolution_chain["id"] = pokemon_data["id"]
                        evolution_chain["name"] = utils.get_translated_field(pokemon_species_data["names"], "name", "es")
                        evolution_chain["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                        evolution_chain["evolves_to"] = []
                        
                        for evolution_1 in start_pokemon["evolves_to"]:
                            evolution_1_dict = {}
                            pokemon_species_url = evolution_1["species"]["url"]
                            pokemon_data = utils.make_pokeapi_call(
                                "https://pokeapi.co/api/v2/pokemon/" + pokemon_species_url.split("/")[6], 
                                "pokemon info - get_evolution_chain() - 1"
                            )
                            if pokemon_data:
                                pokemon_species_data = utils.make_pokeapi_call(pokemon_species_url, "pokemon species - get_evolution_chain() - 1")
                                if pokemon_species_data:
                                    evolution_1_dict["id"] = pokemon_data["id"]
                                    evolution_1_dict["name"] = utils.get_translated_field(pokemon_species_data["names"], "name", "es")
                                    evolution_1_dict["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                                    evolution_1_dict["evolution_details"] = get_evolution_details(evolution_1["evolution_details"])
                                    evolution_1_dict["evolves_to"] = []
                                    for evolution_2 in evolution_1["evolves_to"]:
                                        evolution_2_dict = {}
                                        pokemon_species_url = evolution_2["species"]["url"]
                                        pokemon_data = utils.make_pokeapi_call(
                                            "https://pokeapi.co/api/v2/pokemon/" + pokemon_species_url.split("/")[6], 
                                            "pokemon info - get_evolution_chain() - 2"
                                        )

                                        if pokemon_data:
                                            pokemon_species_data = utils.make_pokeapi_call(pokemon_species_url, "pokemon species - get_evolution_chain() - 2")
                                            if pokemon_species_data:
                                                evolution_2_dict["id"] = pokemon_data["id"]
                                                evolution_2_dict["name"] = utils.get_translated_field(pokemon_species_data["names"], "name", "es")
                                                evolution_2_dict["types"] = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
                                                evolution_2_dict["evolution_details"] = get_evolution_details(evolution_2["evolution_details"])
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


def main():
    utils.create_folders_structure(cfg.pokemon_dirs)
    if not os.path.isdir(cfg.objects_dir):
        os.makedirs(cfg.objects_dir)

    if cfg.remove_pokemon_info:
        utils.remove_dir_files(cfg.pokemon_info_path)
    if cfg.remove_pokemon_evolution_chain:
        utils.remove_dir_files(cfg.pokemon_evolution_chains_path)

    for pokemon_id in range(cfg.pkm_id_start, cfg.pkm_id_end+1): 
        pokemon_info_json = cfg.pokemon_info_path + str(pokemon_id) + ".json"
        if not os.path.isfile(pokemon_info_json):
            pokemon_info = get_pokemon_info(pokemon_id)
            with open (pokemon_info_json, "w") as output_file: 
                json.dump(pokemon_info, output_file)
            print(f"INFO: Se ha guardado el archivo '{pokemon_info_json}' correctamente!")
        else:
            print(f"INFO: El archivo '{pokemon_info_json}' ya existe. Omitiendo...")

        download_pokemon_media(pokemon_id)

        pokemon_evolution_chain, evolution_chain_id = get_evolution_chain(pokemon_id, pokemon_info_json)
        evolution_chain_json = cfg.pokemon_evolution_chains_path + str(evolution_chain_id) + ".json"
        if pokemon_evolution_chain:
            with open (evolution_chain_json, "w") as output_file: 
                json.dump(pokemon_evolution_chain, output_file)
            print(f"INFO: Se ha guardado el archivo '{evolution_chain_json}' correctamente!")
        else:
            print(f"INFO: El archivo '{evolution_chain_json}' ya existe. Omitiendo...")


if __name__ == '__main__':
    main()