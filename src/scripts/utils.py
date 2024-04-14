import os
import requests


def create_folders_structure(folder_list):
    for folder in folder_list:
        if not os.path.isdir(folder):
            os.makedirs(folder)
            

def save_file_from_url(url, output_file):
    if url:
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
    else:
        print("INFO: No se ha proporcionado URL. Omitiendo...")


def get_translated_field(target_list, target_field, lang):
    for entry in target_list:
        if entry["language"]["name"] == lang:
            return entry[target_field]
    
    # If lang not found, try to return english translation
    for entry in target_list:
        if entry["language"]["name"] == "en":
            return entry[target_field]
        
    # return None if lang or english translation are not found
    return None


def remove_dir_files(path):
    for filename in os.listdir(path):
        filepath = path + filename
        if os.path.isfile(filepath):
            os.remove(filepath)
            print("INFO: El archivo '" + filepath + "' se ha eliminado correctamente!")


def make_pokeapi_call(url, call_name_if_error):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"ERROR: Hay un problema al conectarse con la Poke API [{call_name_if_error}].\n{response.raise_for_status()}")
    return None

