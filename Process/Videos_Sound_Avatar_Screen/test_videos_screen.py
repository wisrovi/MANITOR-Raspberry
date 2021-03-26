from Config_Videos_Sound_Screen.Instrucciones_Videos import \
    LISTADO_VIDEOS_INSTRUCCIONES, CHECK_NEW_VIDEO
from util_show_videos import Avatar_video
from Config_Videos_Sound_Screen.Constantes import PATH_VIDEOS, FILE_VIDEO_CONTROL

FOLDER = '../../' + PATH_VIDEOS

import os
import json

if not os.path.isdir(FOLDER):
    print("No se encuentra la carpeta con los recursos", os.getcwd(), FOLDER)
    exit()

avatar_class = Avatar_video(FOLDER)


class File_New_Video(object):
    numero_paso = int()
    visto = bool()

    def __init__(self, number, show):
        self.numero_paso = number
        self.visto = show

    def getJson(self):
        return self.__dict__


def read_video_show():
    data = dict()
    FILE = '../../' + FILE_VIDEO_CONTROL
    if os.path.isfile(FILE):
        with open(FILE) as json_file:
            data = json.load(json_file)
    else:
        print("No existe el archivo ", os.getcwd(), FILE)
    return data


def save_video_show( numero_video: int, visto=False):
    OBJ = File_New_Video(numero_video, visto).getJson()
    with open('../../' + FILE_VIDEO_CONTROL, 'w') as outfile:
        json.dump(OBJ, outfile)


def Contar(*args):
    if avatar_class.instruccion_actual >= len(LISTADO_VIDEOS_INSTRUCCIONES):
        avatar_class.terminar_proceso_avatar()
    else:
        avatar_class.continuar_siguiente_paso_instruccion()


import cv2
import time

cv2.namedWindow("Frame")
cv2.createButton("Contar", Contar, None, cv2.QT_PUSH_BUTTON, 1)

if __name__ == "__main__":
    avatar_class.iniciar_avatar()

    time_delay = time.time()

    while True:
        black_screen, video_inicial_final = avatar_class.proceso()

        if avatar_class.get_primer_inicio_avatar():
            if int(abs((time.time() - time_delay) * 100)) / 100 >= CHECK_NEW_VIDEO:
                time_delay = time.time()
                data = read_video_show()
                if len(data) > 0:
                    print("nuevo video", data)
                    if not data['visto']:
                        util.save_video_show(data['numero_paso'], True)
                        print("Nuevo video mostrar")

                        if data['numero_paso'] < 0:
                            avatar_class.set_instruccion_actual(0)
                        else:
                            if avatar_class.instruccion_actual >= len(LISTADO_VIDEOS_INSTRUCCIONES):
                                avatar_class.terminar_proceso_avatar()
                            else:
                                avatar_class.set_instruccion_actual(data['numero_paso'])
                                avatar_class.continuar_siguiente_paso_instruccion()

        if video_inicial_final is not None:
            pass
            # if avatar_class.get_instruccion_actual() > 0:
            #     font = cv2.FONT_HERSHEY_SIMPLEX
            #     org = (50, 50)
            #     fontScale = 1
            #     color = (255, 0, 0)  # BLue
            #     thickness = 2  # Line thickness
            #     black_screen = cv2.putText(black_screen, INSTRUCCIONES[avatar_class.get_instruccion_actual() - 1]['name'], org,
            #                                     font,
            #                                     fontScale,
            #                                     color,
            #                                     thickness, cv2.LINE_AA)

        cv2.imshow("Frame", black_screen)

        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    avatar_class.cerrar_avatar()
    cv2.destroyAllWindows()
