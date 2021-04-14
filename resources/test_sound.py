#! /usr/bin/env python


#DEVICE = "RPI"
#DEVICE = "PC"

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('id', help='id image')
args = parser.parse_args()

#dialogos = None


class Sonido(object):
    DEVICE = "RPI"
    dialogos = None
    listado_audios = list()

    import os
    from playsound import playsound
    from multiprocessing import Process

    from Instrucciones_Guiones import GUIONES, PATH_VIDEOS

    def __init__(self, path=None, device="RPI", base_path=None):
        if path is None:
            path = self.PATH_VIDEOS

        if base_path is not None:
            self.BASE_PATH = base_path
        else:

            self.BASE_PATH = self.os.getcwd()

        self.dialogos = [path + "p" + str(id_dialogo) + ".wav" for id_dialogo in [diag['id'] for diag in self.GUIONES]]

        self.DEVICE = device

        self.__crear_audios()

    def __crear_audios(self):
        for i, file in enumerate(self.dialogos):
            self.listado_audios.append(    self.Process( target=self.__audio, args=(i,) )    )

    def __audio_rpi(self, id_audio):
        id_audio = int(id_audio)
        path = self.dialogos[id_audio]
        # print(id_audio, path)
        self.os.system('omxplayer ' + path)
        # https://www.raspberrypi.org/forums/viewtopic.php?t=67686

    def __audio_pc(self, id_audio):
        id_audio = int(id_audio)
        path = self.BASE_PATH + "/" + self.dialogos[id_audio]
        print(id_audio, path)
        self.playsound(path)

    def __audio(self, id_audio):
        if self.DEVICE == "RPI":
            self.__audio_rpi(id_audio)
        else:
            self.__audio_pc(id_audio)

    def reproducir(self, id_audio):
        id_audio = int(id_audio)
        if 0 <= id_audio < len(self.dialogos):
            print(id_audio)
            self.listado_audios[id_audio].start()


if __name__ == "__main__":
    s = Sonido(device="PC", path="")
    s.reproducir(args.id)

"""
def crear_lista_audios(path=None):
    global dialogos
    
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

if __name__ == "__main__":
    crear_lista_audios("")

    listado_audios = list()
    listado_audios.append(Process(target=audio, args=(0,)))
    listado_audios.append(Process(target=audio, args=(1,)))
    listado_audios.append(Process(target=audio, args=(2,)))
    listado_audios.append(Process(target=audio, args=(3,)))
    listado_audios.append(Process(target=audio, args=(4,)))
    listado_audios.append(Process(target=audio, args=(5,)))
    listado_audios.append(Process(target=audio, args=(6,)))
    listado_audios.append(Process(target=audio, args=(7,)))
    listado_audios.append(Process(target=audio, args=(8,)))
    listado_audios.append(Process(target=audio, args=(9,)))
    listado_audios.append(Process(target=audio, args=(10,)))

    listado_audios[args.id].start()
"""