from Consult_Microservicios import Consult_Microservicios
from time import time
import config
import requests
from flask import Flask, make_response
import json
from multiprocessing import Process

app = Flask(__name__)

microservicio = Consult_Microservicios()

CHECK_SERVICES = list()
for i in range(1, 8, 1):
    try:
        url = 'http://' + microservicio.get_ip_localhost() + ':500' + str(i)
        DATA = requests.get(url, params={}, timeout=10)
        DATA = DATA.text

        OBJ = dict()
        OBJ['microservicio'] = url
        OBJ['status'] = DATA

        CHECK_SERVICES.append(OBJ)
    except:
        pass

print("*****************************************")
print("*            Microservicios             *")
print(CHECK_SERVICES)
print("*****************************************")

FILE_PERSON = "persona.json"

persona = ["NOMBRE_PERSONA_PASADO",  # 0
           "NOMBRE_PERSONA_ACTUAL",  # 1
           "MISMA_PERSONA:BOOL",  # 2
           "PERSONA_SE_ESTA_MOVIENDO:BOOL",  # 3
           "INICIO_PROCESO:BOOL",  # 4
           "VOLTAJE_BATERIA:FLOAT",  # 5
           "CONTEO_TIEMPO_PASO:FLOAT",  # 6
           "CONTEO_PENALIDADES:INT",  # 7
           "UUID_BEACON:STR"  # 8
           ]

print("persona: ", [value for value in enumerate(persona)])


@app.route('/')
def hola():
    return 'Brain by Wisrovi'


@app.route('/check')
def check():
    OBJ = dict()
    for key, value in enumerate(CHECK_SERVICES):
        OBJ[key] = value
    return make_response(OBJ, 200)


@app.route('/person')
def person():
    OBJ = dict()
    try:
        with open(FILE_PERSON) as json_file:
            OBJ = json.load(json_file)
    except:
        pass
    return make_response(OBJ, 200)


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("Chequeo de los microservicios.")
    OBJ['http://localhost:5008/check'] = options_config

    options_config = list()
    options_config.append("Estatus funcionamiento actual.")
    OBJ['http://localhost:5008/person'] = options_config

    return make_response(OBJ, 200)


def proceso_brain():
    global persona
    time_scan_beacon = time()
    time_read_move_person = time()
    time_save_person = time()

    persona[4] = False
    persona[5] = 0
    persona[7] = 0

    tiempo_siguiente_paso = 0

    while True:
        if (time() - time_scan_beacon) > config.SCAN_TIME:
            time_scan_beacon = time()
            persona_actual, uuid = microservicio.leer_nombre_persona()

            if persona_actual == persona[0]:
                persona[2] = True
            else:
                persona[2] = False

            persona[1] = persona[0]
            persona[0] = persona_actual

            persona[8] = uuid

        if (time() - time_read_move_person) >= config.WAIT_TIME:
            time_read_move_person = time()
            persona[3] = microservicio.hay_movimiento(porcentaje_umbral=config.UMBRAL_SET_MOVE)

            if not persona[4]:  # verifico que el proceso no haya iniciado
                if persona[0] is not None:
                    if len(persona[0]) > 0 and persona[3]:  # miro que haya una persona frente al manitor y esta se haya
                        # movido por primera vez
                        persona[7] = 0  # borro el conteo de penalidades
                        persona[4] = True  # inicio el proceso de lavado de manos
                        persona[5] = 0  # set paso 0
                        microservicio.mostrar_audiovisual(id_audiovisual=persona[5], nombre=persona[0])
                        persona[6] = "3.7"  # VALOR SIMULADO
                        persona[5] = 1  # set paso 1 para contabilizar cuanto tiempo dura en este paso
                        tiempo_siguiente_paso = config.pasos[persona[5]]
            else:
                if not persona[3] or not persona[2]:
                    # no hay movimiento o la persona que inicio el proceso no es la misma a la actual
                    tiempo_siguiente_paso += config.PENALITY_TIME  # penalizo con PENALITY_TIME segundos por alerta no movimiento
                    microservicio.indicar_audio_mueva_manos()
                    microservicio.mostrar_video(id_audiovisual=persona[5], nombre=persona[0])
                    persona[7] += 1  # incremento una penalidad
                    if persona[7] >= config.MAX_NUM_ALERT:
                        persona[7] = 0  # borro el conteo de penalidades
                        persona[4] = False  # Finalizo el proceso
                        microservicio.reportar_vector(uuid=persona[8], voltaje=persona[6])
                        persona[0] = ""  # limpio el nombre actual

        if persona[4]:  # valido que exista un proceso iniciado
            if (time() - persona[6]) >= tiempo_siguiente_paso:
                persona[7] = 0  # borro el conteo de penalidades
                persona[5] += 1  # autorizo el siguiente paso en el lavado de manos
                if persona[5] < len(config.pasos):
                    microservicio.mostrar_audiovisual(id_audiovisual=persona[5], nombre=persona[0])
                    microservicio.guardar_en_vector(id_paso=persona[5] - 1, tiempo=tiempo_siguiente_paso)
                    tiempo_siguiente_paso = config.pasos[persona[5]]  # seteo el tiempo minimo para el siguiente paso
                else:
                    persona[4] = False  # Finalizo el proceso
                    microservicio.reportar_vector(uuid=persona[8], voltaje=persona[6])
                    persona[0] = ""  # limpio el nombre actual

        if (time() - time_save_person) >= config.WAIT_SAVE:
            time_save_person = time()
            OBJ = dict()
            OBJ[
                'status_scan_person'] = f"before: {persona[0]} vs now: {persona[1]} -> status (equals): {str(persona[2])}"
            OBJ['uuid_cardholder_now'] = str(persona[8])
            OBJ['battery_voltaje_cardholder'] = str(persona[5])
            OBJ['move'] = str(persona[3])
            OBJ['active_hand_washing_process'] = str(persona[4])
            OBJ['time_for_this_step'] = f"time_step: {str(persona[6])} vs penalities: {str(persona[7])}"
            with open(FILE_PERSON, 'w') as outfile_beacon_scan:
                json.dump(OBJ, outfile_beacon_scan)


Process(target=proceso_brain).start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5008)
