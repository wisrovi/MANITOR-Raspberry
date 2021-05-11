import cv2

from Lienzo import Lienzo, Video
from Sincro import Sincro
from Util import Util
from time import time
from multiprocessing import Process

util = Util()


tiempo_paso = 100
tiempo_inicial = time()
video = None
crono = None
esperando_siguiente_paso = False


def activar_nuevo_video(ID_PASO = 1):
    global tiempo_paso
    global tiempo_inicial
    global video
    global crono
    global esperando_siguiente_paso
    tiempo_paso = Sincro[str(ID_PASO)]['time']
    crono = Sincro[str(ID_PASO)]['cronometro']
    video = Sincro[str(ID_PASO)]['video']
    print("[time]:", util.Leer_HoraActual())
    print("[Video]: ", video)
    print("[Crono]: ", crono)
    print("[delay]: ", tiempo_paso)
    print()
    tiempo_inicial = time()
    esperando_siguiente_paso = False


def video_interfaz():
    activar_nuevo_video(1)

    global esperando_siguiente_paso
    video_instruccion = Video()
    cronometro = Video()

    ancho_pantalla, alto_pantalla = util.screen_size()
    ancho_pantalla, alto_pantalla = int(ancho_pantalla * 0.4), int(alto_pantalla * 0.4)  # solo demo

    LIENZO_MOSTRAR_VIDEOS = (alto_pantalla, ancho_pantalla)  # pixeles (alto, ancho)

    lienzo = Lienzo(LIENZO_MOSTRAR_VIDEOS)
    lienzo.PORCENTAJE_SUPERIOR = 0.9
    lienzo.PORCENTAJE_LATERAL = 0.94
    lienzo.create_board()

    video_poner = lienzo.get_void_board()
    crono_poner = lienzo.get_void_board()
    nombre_poner = lienzo.get_void_board()
    titulo_poner = lienzo.get_void_board()

    while True:
        board = lienzo.get_board()

        if ((time() - tiempo_inicial) >= tiempo_paso) and not esperando_siguiente_paso:
            video_poner = lienzo.get_void_board()
            crono_poner = video_poner
            nombre_poner = video_poner
            titulo_poner = video_poner
            esperando_siguiente_paso = True
            print("Limpiando pantalla")
        else:
            if not esperando_siguiente_paso:
                hay_image, image = video_instruccion.read()
                if hay_image:
                    video_poner = image
                else:
                    video_instruccion = cv2.VideoCapture(video)

                hay_image, image = cronometro.read()
                if hay_image:
                    crono_poner = image
                else:
                    cronometro = cv2.VideoCapture(crono)

        # print(video_poner)
        # print(crono_poner)
        lienzo.poner_cronometro(crono_poner)
        lienzo.poner_instruccion(video_poner)
        lienzo.poner_nombre(nombre_poner)
        lienzo.poner_titulo(titulo_poner)

        cv2.imshow("Frame", board)
        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    try:
        video_instruccion.release()
        cronometro.release()
    except:
        pass
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Process(target=video_interfaz).start()
