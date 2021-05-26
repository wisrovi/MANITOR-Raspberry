import cv2

from Lienzo import Lienzo, Video
from Sincro import Sincro
from Util import Util
from time import time
from multiprocessing import Process, Queue
from flask import Flask, request
import json
app = Flask(__name__)

util = Util()
pqueue = Queue()


tiempo_paso = 100
tiempo_inicial = time()
video = None
crono = None
esperando_siguiente_paso = False

PANTALLA_COMPLETA = False
if PANTALLA_COMPLETA:
    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def leer_cola():
    if not pqueue.empty():
        data_complete = dict()
        for _ in range(pqueue.qsize()):
            data = pqueue.get()
            for key, value in data.items():
                # print(key, value)
                data_complete[key] = value
        return data_complete
    else:
        return dict()


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
    # ancho_pantalla, alto_pantalla = int(ancho_pantalla * 0.4), int(alto_pantalla * 0.4)  # solo demo

    LIENZO_MOSTRAR_VIDEOS = (alto_pantalla, ancho_pantalla)  # pixeles (alto, ancho)

    lienzo = Lienzo(LIENZO_MOSTRAR_VIDEOS)
    lienzo.PORCENTAJE_SUPERIOR = 0.9
    lienzo.PORCENTAJE_LATERAL = 0.94
    lienzo.create_board()

    video_poner = lienzo.get_void_board()
    crono_poner = lienzo.get_void_board()
    nombre_poner = lienzo.get_void_board()
    titulo_poner = lienzo.get_void_board()

    nombre_mostrar = None
    while True:
        data = leer_cola()
        if len(data) > 0 :
            id = data.get('id')
            name = data.get('name')
            print("[queue]:", id)
            print("[queue]:", name)
            print()
            if id is not None:
                activar_nuevo_video(int(id))

        board = lienzo.get_board()

        if ((time() - tiempo_inicial) >= tiempo_paso) and not esperando_siguiente_paso:
            video_poner = lienzo.get_void_board()
            crono_poner = video_poner
            nombre_poner = video_poner
            titulo_poner = video_poner
            esperando_siguiente_paso = True
            print("Limpiando pantalla")
        else:
            hay_image, image = video_instruccion.read()
            if not esperando_siguiente_paso:
                if hay_image:
                    video_poner = image
                else:
                    video_instruccion = cv2.VideoCapture(video)

            hay_image, image = cronometro.read()
            if not esperando_siguiente_paso:
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


@app.route('/')
def hola():
    return 'Interfaz visual by Wisrovi'


@app.route('/mostrar', methods=['GET'])
def mostrar():
    id = request.args.get('id')
    name = request.args.get('name')

    if id is not None and name is not None:
        OBJ = dict()
        OBJ['id'] = id
        OBJ['name'] = name
        pqueue.put(OBJ)
        return json.dumps(OBJ, indent=4)

    return "no hay dados ingresados, por favor consulte /help las opciones de variables a usar"


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("muestra un video dentro del banco de videos, el nombre de la persona y un texto con el paso a seguir")
    options_config.append("<id>: indica el id del video")
    options_config.append("<name>: indica el nombre a mostrar en la interfaz grafica")
    OBJ['http://localhost:5005/mostrar?id=<id>&name=<name>'] = options_config

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    Process(target=video_interfaz).start()
    app.run(host="0.0.0.0", port=5005)
    print("[system]: started")
