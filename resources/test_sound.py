#! /usr/bin/env python
from Instrucciones_Guiones import GUIONES, PATH_VIDEOS

DEVICE = "RPI"
DEVICE = "PC"

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('id', help='id image')
args = parser.parse_args()

dialogos = None


def crear_lista_audios(path=None):
    global dialogos
    if path is None:
        path = PATH_VIDEOS
    dialogos = [path + "p" + str(id_dialogo) + ".wav" for id_dialogo in [diag['id'] for diag in GUIONES]]
    print(dialogos)


from multiprocessing import Process

if DEVICE == "RPI":
    import os


    def audio(id_audio=0):
        id_audio = int(id_audio)
        path = dialogos[id_audio]
        # print(id_audio, path)
        os.system('omxplayer ' + path)
        # https://www.raspberrypi.org/forums/viewtopic.php?t=67686
else:
    from playsound import playsound


    def audio(id_audio=0):
        id_audio = int(id_audio)
        path = dialogos[id_audio]
        # print(id_audio, path)
        playsound(path)

crear_lista_audios("")
Process(target=audio, args=(args.id,)).start()
