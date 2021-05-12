from multiprocessing import Process

from Process.Sound.config_sound import TIME_SCAN_FILE_SOUND
from Process.Util.Util import Util
from resources.Instrucciones_Guiones import PATH_VIDEOS, GUIONES
from resources.test_sound import Sonido


def main_sonido():
    import os
    import time
    base_folder = os.getcwd() + "/" + PATH_VIDEOS

    util = Util()
    print(base_folder)
    s = Sonido(base_path=base_folder, path=PATH_VIDEOS, guiones=GUIONES)
    while True:
        time.sleep(TIME_SCAN_FILE_SOUND)
        OBJ = util.read_data_scan_sound()
        if not OBJ['visto']:
            id_audio = OBJ['numero_audio']
            print("audio: ", id_audio)
            util.save_audio_show(int(OBJ['numero_audio']), True)
            try:
                s.reproducir(id_audio)
            except:
                pass


if __name__ == "__main__":
    p = Process(target=main_sonido)

    p.start()