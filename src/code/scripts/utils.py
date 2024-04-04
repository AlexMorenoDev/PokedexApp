import os
import requests


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


def get_translated_field(target_list, target_field, lang):
    for entry in target_list:
        if entry["language"]["name"] == lang:
            return entry[target_field]
    return None


def remove_dir_files(path):
    for filename in os.listdir(path):
        filepath = path + filename
        if os.path.isfile(filepath):
            os.remove(filepath)
            print("INFO: El archivo '" + filepath + "' se ha eliminado correctamente!")

