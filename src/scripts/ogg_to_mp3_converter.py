import os
# https://github.com/jiaaro/pydub
from pydub import AudioSegment

# TO SAVE MP3 FILES, FFMPEG MUST BE INSTALLED ON THE DEVICE
# For Windows: https://phoenixnap.com/kb/ffmpeg-windows
def ogg_to_mp3(target_file, output_file):
    sound = AudioSegment.from_file(target_file)
    sound.export(output_file, format="mp3", bitrate="128k")
    print("Se ha guardado correctamente el archivo '" + output_file + "'")


def main():
    target_folder = "../../static/pokemon/cries/ogg/"
    output_folder = "../../static/pokemon/cries/mp3/"

    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(target_folder):
        input_file = target_folder + filename
        if os.path.isfile(input_file):
            output_file = output_folder + filename.split(".")[0] + ".mp3"
            if not os.path.isfile(output_file):
                ogg_to_mp3(input_file, output_file)
            else:
                print("El archivo '" + output_file + "' ya existe. Omitiendo...")


if __name__ == '__main__':
    main()