class Sonido(object):
    from playsound import playsound
    from concurrent.futures import ThreadPoolExecutor

    from Instrucciones_Guiones import GUIONES, PATH_VIDEOS

    dialogos = list()

    def __init__(self, path=None):
        if path is None:
            path = self.PATH_VIDEOS
        self.dialogos = [path + "p" + str(id_dialogo) + ".wav" for id_dialogo in [diag['id'] for diag in self.GUIONES]]

    def __reproducir_audio(self, id_audio):
        if id_audio > len(self.dialogos):
            id_audio = len(self.dialogos)
        audio = self.dialogos[id_audio]
        self.playsound(audio)

    def reproducir(self, id_audio):
        currs = self.ThreadPoolExecutor(max_workers=5)
        currs.submit(self.__reproducir_audio, id_audio)


if __name__ == "__main__":
    s = Sonido()
    s.reproducir(0)

    import time
    time.sleep(5)

    s.reproducir(2)
