import os
import gdown
import patoolib

# Model can be initialized executing "init_model.py" script or executing this script to download a rar file with the model already initialized
# When deploying the application, as the "init_model.py" takes so much time to finish, second option will be done
def main():
    url = "https://drive.google.com/uc?id=" + os.environ["gdrive_file_id"]
    download_output = "../static/pokemon.rar" # For deployment
    #download_output = "../../static/pokemon.rar" # For localhost
    gdown.download(url, download_output, quiet=False)

    extract_output = "../static/" # For deployment
    #extract_output = "../../static/" # For localhost
    patoolib.extract_archive(download_output, outdir=extract_output)
    os.remove(download_output)


if __name__ == '__main__':
    main()