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


def get_pokemon_info(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    res_pokemon_info = requests.get(url)
    
    if res_pokemon_info.status_code == 200:
        pokemon_data = res_pokemon_info.json()

        # Get pokemon generic info
        pokemon_info = {
            "id": pokemon_id,
            "name": pokemon_data["name"], 
            "height": pokemon_data["height"], 
            "weight": pokemon_data["weight"], 
            #"abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]], 
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        }

        # Download pokemon cry and sprites only if they dont exist
        save_file_from_url(pokemon_data["cries"]["latest"], f"../static/pokemon/cries/{pokemon_id}.ogg")
        save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_default"], f"../static/pokemon/images/normal/{pokemon_id}.png")
        save_file_from_url(pokemon_data["sprites"]["other"]["official-artwork"]["front_shiny"], f"../static/pokemon/images/shiny/{pokemon_id}.png" )

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
    

def main():
    pkm_id_start = 1
    pkm_id_end = 151

    create_folders_structure([
        "../static/pokemon/cries/", 
        "../static/pokemon/images/normal/", 
        "../static/pokemon/images/shiny/",
        "../static/pokemon/info/"
        ]
    )

    for i in range(pkm_id_start, pkm_id_end+1): 
        pokemon_info = get_pokemon_info(i)
        with open (f"../static/pokemon/info/{i}.json", "w") as output_file: 
            json.dump(pokemon_info, output_file)
        print(f"INFO: Se ha guardado el archivo '{i}.json' correctamente!")
        

if __name__ == '__main__':
    main()