import threading

from Consult_Microservicios import Consult_Microservicios
from time import time, sleep
import config
import requests
from flask import Flask, make_response
import json
from multiprocessing import Process

app = Flask(__name__)

microservicio = Consult_Microservicios()

CHECK_SERVICES = list()
CHECK_SERVICES_BAD = list()
ALL_MICROSERVICES_RUN = True
for i in range(1, 8, 1):
    url = 'http://' + microservicio.get_ip_localhost() + ':500' + str(i)
    try:
        DATA = requests.get(url, params={}, timeout=10)
        DATA = DATA.text

        OBJ = dict()
        OBJ['microservicio'] = url
        OBJ['status'] = DATA

        CHECK_SERVICES.append(OBJ)
    except:
        CHECK_SERVICES_BAD.append(url)
        print("[error]: ", url)
        ALL_MICROSERVICES_RUN = False

print("*****************************************")
print("*            Microservicios             *")
for service in CHECK_SERVICES:
    print(service)
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
           "UUID_BEACON:STR",  # 8
           "UUID_BEACON_UUID_LAST:STR"  # 9
           ]

# print("persona: ", [value for value in enumerate(persona)])

print()
print("Sistema iniciado")
print()


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
    print("Subproceso iniciado")
    time_scan_beacon = time()
    time_read_move_person = time()
    time_save_person = time()

    persona[4] = False
    persona[5] = 0
    persona[7] = 0
    persona[0] = ""

    tiempo_siguiente_paso = 0

    microservicio.mostrar_video(id_audiovisual=0,
                                nombre="")  # limpio la pantalla de interfaz_video y borro el nombre de la persona

    while True:
        if ALL_MICROSERVICES_RUN:
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
                hay_movimiento = microservicio.hay_movimiento(porcentaje_umbral=config.UMBRAL_SET_MOVE)
                if hay_movimiento is not None:
                    persona[3] = hay_movimiento

                if not persona[4]:  # verifico que el proceso no haya iniciado
                    hay_persona = persona[0] is not None
                    hay_uuid_cardholder = persona[8] is not None
                    if hay_persona and hay_uuid_cardholder:
                        if len(persona[0]) > 0 and persona[3]:  # miro que haya una persona frente al manitor y esta se haya
                            # movido por primera vez
                            persona[7] = 0  # borro el conteo de penalidades
                            persona[4] = True  # inicio el proceso de lavado de manos
                            persona[5] = 0  # set paso 0
                            microservicio.mostrar_audiovisual(id_audiovisual=persona[5], nombre=persona[0])
                            persona[5] = "3.7"  # VALOR SIMULADO DE VOLTAJE
                            persona[6] = 1  # set paso 1 para contabilizar cuanto tiempo dura en este paso
                            persona[9] = (persona[0], persona[8])
                            tiempo_siguiente_paso = time()
                else:
                    misma_persona = persona[2]
                    la_persona_se_fue = (persona[0] == persona[1]) and persona[0] is None
                    hay_movimiento_cam = persona[3]
                    if (la_persona_se_fue and not misma_persona) or not hay_movimiento_cam:
                        # no hay movimiento o la persona que inicio el proceso no es la misma a la actual
                        tiempo_siguiente_paso += config.PENALITY_TIME  # penalizo con PENALITY_TIME segundos por alerta no movimiento
                        microservicio.indicar_audio_mueva_manos()  # indicar audio alerta, para que la persona mueva las manos
                        persona[7] += 1  # incremento una penalidad
                        sleep(2)  # pausa para que no salgan alertas muy seguidas
                        if persona[7] >= config.MAX_NUM_ALERT:
                            persona[7] = 0  # borro el conteo de penalidades
                            persona[4] = False  # Finalizo el proceso
                            microservicio.reportar_vector(uuid=persona[9][1], voltaje=persona[9][0])
                            persona[0] = None  # limpio el nombre actual
                            persona[1] = None  # limpio el nombre actual
                            microservicio.mostrar_video(id_audiovisual=0, nombre="")   # limpio la pantalla de interfaz_video y borro el nombre de la persona
                            sleep(config.TIME_NEXT_PERSON)  # espero un tiempo antes de procesar a otra persona

            if persona[4]:  # valido que exista un proceso iniciado
                if (time() - tiempo_siguiente_paso) >= config.pasos[persona[6]]:
                    persona[7] = 0  # borro el conteo de penalidades
                    persona[6] += 1  # autorizo el siguiente paso en el lavado de manos
                    if persona[6] < len(config.pasos):
                        microservicio.mostrar_audiovisual(id_audiovisual=persona[6], nombre=persona[0])
                        microservicio.guardar_en_vector(id_paso=persona[6] - 1, tiempo=tiempo_siguiente_paso)
                        tiempo_siguiente_paso = time()  # seteo el tiempo minimo para el siguiente paso
                    else:
                        persona[6] = 0
                        persona[4] = False  # Finalizo el proceso

                        persona_uso_manitor = persona[8]
                        uuid_uso_manitor = persona[6]
                        if persona_uso_manitor is None:
                            persona_uso_manitor = persona_uso_manitor
                        if uuid_uso_manitor is None:
                            uuid_uso_manitor = persona[9][0]
                        microservicio.reportar_vector(uuid=persona_uso_manitor, voltaje=uuid_uso_manitor)

                        persona[0] = None  # limpio el nombre actual
                        persona[1] = None  # limpio el nombre actual
                        microservicio.mostrar_video(id_audiovisual=0, nombre="")  # limpio la pantalla de interfaz_video y borro el nombre de la persona
                        sleep(config.TIME_NEXT_PERSON)   # espero un tiempo antes de procesar a otra persona

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
        else:
            print("*****************************************")
            print("*         Check Microservicios          *")
            for service in CHECK_SERVICES_BAD:
                print(service)
            print("*****************************************")
            print()
            sleep(60)


print("Lanzando subproceso")
# Process(target=proceso_brain).start()
threading.Thread(target=proceso_brain).start()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5008)
