from playsound import playsound

# from library_reproduce_audio.SoundUtil import Sonido
from concurrent.futures import ThreadPoolExecutor


def reproducir_audio(path_audio="p0.mp3"):
    playsound(path_audio)


if __name__ == "__main__":
    path_audio = "p0.mp3"


    #currs = ThreadPoolExecutor(max_workers=5)
    #currs.submit(reproducir_audio, path_audio)

    reproducir_audio(path_audio)

