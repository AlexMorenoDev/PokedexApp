import os
import gdown
import patoolib


def main():
    url = "https://drive.google.com/uc?id=1g3KOhSVoc6YUkVGwIqDuTpksYI43OMJG"
    download_output = "../../static/pokemon.rar"
    gdown.download(url, download_output, quiet=False)
    patoolib.extract_archive(download_output, outdir="../../static/")
    os.remove(download_output)


if __name__ == '__main__':
    main()