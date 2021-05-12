import os

from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import json
from os import remove
import datetime
import time
from multiprocessing import Process, Queue

pqueue = Queue()

from config_movimiento_frente_camara import FILE_CONFIG_MOVE_DETECT, constante_cambio_area


##################################################################
#                                                                #
#                                                                #
#                                                                #
#                                                                #
#                                                                #
#             Proceso detectar movimiento color piel             #
#                                                                #
#                                                                #
#                                                                #
#                                                                #
##################################################################


def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


def CreateColor(h=0, s=0, v=0):
    # HSV -> H[0 a 179], S[0 a 255], V[0 a 255]
    return np.array([h, s, v])


def leer_configuracion():
    try:
        OBJ = dict()
        with open(FILE_CONFIG_MOVE_DETECT) as json_file:
            OBJ = json.load(json_file)

        piel = (
            CreateColor(OBJ["H_min"], OBJ["S_min"], OBJ["V_min"]),
            CreateColor(OBJ["H_max"], OBJ["S_max"], OBJ["V_max"]))

        franja_colores = {
            "min": piel[0],
            "max": piel[1]
        }

        return franja_colores
    except:
        return {}


def CrearMascara(frame, franja_colores):
    masking = None
    if frame is not None:
        # convierto la imagen a HSV para quitar capas y mejorar el procesamiento
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Creo una mascara, donde pinto en blanco el color a buscar (color piel) y en negro lo que no cumpla dentro del color de interes
        masking = cv2.inRange(hsv_img, franja_colores["min"], franja_colores["max"])

        # cv2.imshow("Deteccion Color", masking)
    return masking


def QuitarPartesNoMarcadasEnMascara(frame, masking):
    # Creo una nueva imagen tomando la imagen original y dejando solo las partes blancas de la mascara
    new_img = cv2.bitwise_and(frame, frame, mask=masking)
    return new_img


last_areas = list()


def hallar_contornos_areas(frame, masking):
    global last_areas
    thresh = cv2.threshold(masking, 25, 255, cv2.THRESH_BINARY)[
        1]  # (masking,127,255,   0) # Aplicamos un umbral para quitar ruido
    thresh = cv2.dilate(thresh, None, iterations=2)  # Dilatamos el umbral para tapar agujeros

    contornos = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[
        0]  # CHAIN_APPROX_SIMPLE: deja solo los contornos externos obviando los internos (ahorrar memoria y aumentar velocidad computo)

    cajas = list()
    areas = list()
    contornos_finales = list()
    for c in contornos:  # Recorremos todos los contornos encontrados
        if cv2.contourArea(c) < constante_cambio_area:  # Eliminamos los contornos mas pequenos
            continue
        (x, y, w, h) = cv2.boundingRect(
            c)  # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cajas.append((x, y, x + w, y + h))
        contornos_finales.append(c)

        area = w * h
        areas.append(area)

    cv2.drawContours(frame, contornos_finales, -1, (255, 0, 0), 3)

    # Determinar movimiento de acuerdo a el cambio de areas (superior a una constante definida) en objeto(s) en la escena
    hay_movimiento_segun_cambio_areas = False
    if len(last_areas) == len(
            areas):  # if exist(True) in list(  if abs(valor)>constante*1.5 => valor = resta(last_areas, areas)  )
        hay_movimiento_segun_cambio_areas = True if True in [True if i > constante_cambio_area * 1.5 else False
                                                             for i in
                                                             [abs(i) for i in [e1 - e2 for e1, e2 in
                                                                               zip(last_areas,
                                                                                   areas)]]] else False
    else:
        hay_movimiento_segun_cambio_areas = True
        pass
    last_areas = areas

    return cajas, areas, hay_movimiento_segun_cambio_areas


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


def main_move_detect_process(ver=True):
    global pqueue
    movimiento = 0

    franja_colores = leer_configuracion()
    if len(franja_colores) == 0:
        print("No existe archivo de configuracion")

    cap = cv2.VideoCapture(0)

    tiempo_report = time.time()

    while True:
        hay_imagen, frame = cap.read()
        if hay_imagen:
            if ver:
                cv2.imshow("Original Image", frame)

            masking = CrearMascara(frame, franja_colores)
            frame = QuitarPartesNoMarcadasEnMascara(frame, masking)
            cajas, areas, hay_movimiento_segun_cambio_areas = hallar_contornos_areas(frame, masking)
            if hay_movimiento_segun_cambio_areas:
                cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)
                movimiento += 1
                movimiento = 100 if movimiento > 100 else movimiento
            else:
                movimiento -= 1
                movimiento = 0 if movimiento < 0 else movimiento
                cv2.circle(frame, (50, 50), 20, (255, 0, 255), -1)

            if ver:
                cv2.imshow("Image", frame)
            else:
                remove('static/move.jpg')
                cv2.imwrite('static/move.jpg', frame)
                # print("save image")

            if (time.time() - tiempo_report) > 0.1:
                tiempo_report = time.time()
                # print(Leer_HoraActual(), movimiento)
                OBJ = dict()
                OBJ['time'] = Leer_HoraActual()
                OBJ['move'] = movimiento
                pqueue.put(OBJ)
                # print("save")

        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()


Process(target=main_move_detect_process, args=(False,)).start()

##################################################################
#                                                                #
#                                                                #
#                                                                #
#                                                                #
#                                                                #
#                    Proceso del servicio                        #
#                                                                #
#                                                                #
#                                                                #
#                                                                #
##################################################################


app = Flask(__name__)


@app.route('/')
def hola():
    return 'Move Detect by Wisrovi'


@app.route('/cam')
def cam():
    return render_template('cam.html')


@app.route('/move', methods=['GET'])
def move():
    umbral = request.args.get('umbral')
    if umbral is None:
        umbral = 60
    else:
        umbral = int(umbral)
    data = leer_cola()
    print(data)

    if len(data) > 0:
        OBJ = dict()
        OBJ['acc'] = data['move']
        OBJ['time'] = Leer_HoraActual()
        OBJ['move'] = 1 if data['move'] >= umbral else 0
        return jsonify(OBJ)
    else:
        return "Error"


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("Devuelve el estatus de movimiento (si hay)")
    options_config.append("umbral = valor minimo de precision requerida (%) [0 - 100], el valor por default es 60 (%)")
    OBJ['http://localhost:5006/move?umbral=<umbral>'] = options_config

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
