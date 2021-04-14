from Manitor.Manitor import MANITOR
from Process.Move_Person_Fron_Cam.DetectMoveSkinUtil import Deteccion_movimiento
from Process.Move_Person_Fron_Cam.config_movimiento_frente_camara import \
    TIEMPO_DESCANSO_ENTRE_UNA_PERSONA_Y_OTRA_CUANDO_LA_PRIMERA_COMPLETO_DESINFECCION, FILE_CONFIG_MOVE_DETECT
from Process.Util.Util import Util
from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import \
    LISTADO_VIDEOS_INSTRUCCIONES
import os

VIDEO = [i for i in range(len(LISTADO_VIDEOS_INSTRUCCIONES))]

manitor = MANITOR()


def corrimiento(lista, data):
    lista.reverse()
    lista.append(data)
    lista.reverse()
    return lista[:-1]


def main_move_detect():
    MOSTRAR_FRAME = False
    import cv2
    import time

    class Proceso_deteccion_movimiento(object):
        import time

        id_video = int(-1)
        time_elapsed = float()

        def __init__(self):
            self.util = Util()

        def iniciar_proceso(self):
            print("[main_move_detect]:", "Proceso iniciado")
            self.time_elapsed = self.time.time()

        def primer_movimiento_detectado(self):
            print("[main_move_detect]:", "Primer movimiento")
            self.util.save_audio_show(0)
            self.id_video = 0
            manitor.video_instruccion_mostrar_video(self.id_video)
            self.time_elapsed = self.time.time()

        def primer_preaviso_no_movimiento(self):
            print("[main_move_detect]:", "Primer preaviso")
            self.util.save_audio_show(12)

        def segundo_preaviso_no_movimiento(self):
            print("[main_move_detect]:", "Segundo preaviso")
            self.util.save_audio_show(12)

        def tercer_preaviso_no_movimiento(self):
            print("[main_move_detect]:", "Tercer preaviso, por favor repita la instruccion")
            self.util.save_audio_show(13)
            self.id_video -= 1
            if self.id_video < 0:
                self.id_video = 0
            dm.reiniciar_tiempo_instruccion()
            self.mostrar_siguiente_video(False)

        def mostrar_siguiente_video(self, conteo_tiempo=True):
            tiempo = int(abs(self.time_elapsed - self.time.time()) * 100) / 100

            self.id_video += 1
            if self.id_video >= len(LISTADO_VIDEOS_INSTRUCCIONES):
                self.id_video = -1
                manitor.reportar_correcto_lavado_manos(historico[0])
                manitor.video_instruccion_mostrar_video(self.id_video)
                dm.set_time(TIEMPO_DESCANSO_ENTRE_UNA_PERSONA_Y_OTRA_CUANDO_LA_PRIMERA_COMPLETO_DESINFECCION)
            else:
                id_este_video, nuevo_tiempo, name = manitor.get_data_video(self.id_video)
                if id_este_video == self.id_video:
                    dm.set_time(nuevo_tiempo)
                    manitor.video_instruccion_mostrar_video(self.id_video)

                if conteo_tiempo:
                    print("[main_move_detect]:", tiempo, ":", "Siguiente instruccion:", name)
                    self.time_elapsed = self.time.time()

            self.util.save_audio_show(self.id_video)

        @staticmethod
        def proceso_interrumpido_por_superar_tres_advertencias():
            print("[main_move_detect]:", "Proceso terminado")

    dm = Deteccion_movimiento(cam=0, clase=Proceso_deteccion_movimiento)

    time_elapsed = time.time()

    historico = ["" for _ in range(15)]
    while True:
        if (int(abs(time_elapsed - time.time()) * 100) / 100) >= 5:
            time_elapsed = time.time()

            lectura_scan_beacon = sorted(
                [(data_json['rssi'], uuid) for uuid, data_json in manitor.read_beacons().items()], key=lambda x: x[0],
                reverse=True)
            mas_cercano = lectura_scan_beacon[0] if len(lectura_scan_beacon) > 0 else (None, "")
            historico = corrimiento(historico, mas_cercano[1])
            # print( True if (historico[0]==historico[1] and len(historico[1])>0) else False ,list(map(lambda x: x[:8], list(filter(lambda x: len(x) > 8, historico)))))
            if historico[0] == historico[1] and len(historico[1]) > 0:
                if not dm.hay_movimiento():
                    dm.iniciar_proceso_deteccion_movimiento()
            else:
                dm.terminar_proceso_deteccion_movimiento()

        frame = dm.get_frame()
        if MOSTRAR_FRAME:
            cv2.imshow("frame", frame)

        time.sleep(0.025)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    dm.cerrar_camara()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    from decouple import config

    print()
    print("*********************************************************")
    print("*\t", "Autor: " "\t\t\t\t\t\t\t\t\t\t\t*")
    print("*\t", config('autor', default=''), "\t\t\t\t*")
    print("*\t", config('alias_autor', default=''), "\t\t\t\t\t\t\t\t\t\t\t*")
    print("*\t", config('email_autor', default=''), "\t\t\t\t\t\t*")
    print("*\t", config('linkedin_autor', default=''), "\t*")
    print("*********************************************************")

    BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + "/Process/Move_Person_Fron_Cam/"
    FILE = BASE_DIR + FILE_CONFIG_MOVE_DETECT
    if os.path.isfile(FILE):
        main_move_detect()
    else:
        print(
            "No existe el archivo de configuracion para detectar el movimiento, por favor validelo o creelo con '{}CREATE_file_config_color.py'".format(
                BASE_DIR))
