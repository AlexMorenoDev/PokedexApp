import os
import gdown
import patoolib

# Model can be initialized executing "init_model.py" script or executing this script to download a rar file with the model already initialized
# When deploying the application, as the "init_model.py" takes so much time to finish, second option will be done
def main():
    # Key: environment variable name | value: zip filename
    file_dict = {
        "pokemon_gdrive_file_id": "pokemon.zip",
        "objects_gdrive_file_id": "objects.zip"
    }

    for key, value in file_dict.items():
        url = "https://drive.google.com/uc?id=" + os.environ[key]
        extract_output = "../static/" # For deployment
        #extract_output = "../../static/" # For localhost
        download_output = extract_output + value
        gdown.download(url, download_output, quiet=False)
        patoolib.extract_archive(download_output, outdir=extract_output)
        os.remove(download_output)


if __name__ == '__main__':
    main()