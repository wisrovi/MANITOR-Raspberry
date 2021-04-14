from resources.Instrucciones_Guiones import GUIONES, PATH_VIDEOS


class Sonido(object):
    from playsound import playsound

    dialogos = list()

    def __init__(self, path=None):
        if path is None:
            path = PATH_VIDEOS
        self.dialogos = [path + "p" + str(id_dialogo) + ".wav" for id_dialogo in [diag['id'] for diag in GUIONES]]
        # print(self.dialogos)

    def __reproducir_audio(self, id_audio):
        if id_audio > len(self.dialogos):
            id_audio = len(self.dialogos)
        audio = self.dialogos[id_audio]

        audio = "../p0.mp3"
        self.playsound(audio)
        print(audio)

    def reproducir(self, id_audio):
        self.__reproducir_audio(0)
        #currs = self.ThreadPoolExecutor(max_workers=5)
        #currs.submit(self.__reproducir_audio, id_audio)


if __name__ == "__main__":
    s = Sonido("../../resources/")
    s.reproducir(0)
