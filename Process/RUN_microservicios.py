import json
import os
import cv2
import time
from multiprocessing import Process

from Beacon_scan.ScanUtility import beacontools
from Beacon_scan.config_beacon import TIME_SCAN, NAME_FILE_BEACON
from Mqtt.MqttUtil import Mqtt
from Advanced_features import Orden_mqtt_recibida
from Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Constantes import PATH_VIDEOS
from Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import \
    LISTADO_VIDEOS_INSTRUCCIONES, CHECK_NEW_VIDEO
from Videos_Sound_Avatar_Screen.util_show_videos import Avatar_video
from Util.Util import Util

FOLDER = '../' + PATH_VIDEOS
avatar_class = Avatar_video(FOLDER)
util = Util()
scan_beacon = beacontools(0, TIME_SCAN)
mqtt = Mqtt(Orden_mqtt_recibida)


def main_videos():
    avatar_class.iniciar_avatar()

    time_delay = time.time()

    while True:
        black_screen, video_inicial_final = avatar_class.proceso()

        if avatar_class.get_primer_inicio_avatar():
            if int(abs((time.time() - time_delay) * 100)) / 100 >= CHECK_NEW_VIDEO:
                time_delay = time.time()
                data = util.read_video_show()
                if len(data) > 0:
                    # print("nuevo video", data)
                    if not data['visto']:
                        util.save_video_show(data['numero_paso'], True)
                        print("[main_videos]:", "Nuevo video mostrar")

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


def main_beacon_scan():
    PRINT_LOG = False
    scan_beacon.start_continue_process()
    while True:
        BEACONS = scan_beacon.get_beacons()

        OBJ = dict()
        for key, beacon_class in BEACONS.items():
            OBJ[key] = beacon_class.getJson()
            if PRINT_LOG:
                print("[main_beacon_scan]:",beacon_class.getJson())

        if PRINT_LOG:
            print("[main_beacon_scan]:","Escaneando")

        with open("../../" + NAME_FILE_BEACON, 'w') as outfile:
            json.dump(OBJ, outfile)

        time.sleep(TIME_SCAN)
    scan_beacon.detener_continue_process()


def main_mqtt():
    while True:
        time.sleep(3)
        data = mqtt.read_file()
        if len(data) > 0:
            print(data)
            mqtt.EnviarCardHolder(data['uuid'])
    mqtt.FinalizarEscuchaMQTT()


if __name__ == "__main__":
    if not os.path.isdir(FOLDER):
        print("No se encuentra la carpeta con los recursos", os.getcwd(), FOLDER)
        proceso_videos = Process(target=main_videos)
        proceso_videos.start()

    proceso_beacon_scan = Process(target=main_beacon_scan)
    proceso_beacon_scan.start()

    proceso_mqtt = Process(target=main_mqtt)
    proceso_mqtt.start()
