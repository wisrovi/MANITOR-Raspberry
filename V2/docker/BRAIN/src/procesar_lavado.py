from secuencia_lavado import secuencia_lavado
from evaluar_movimiento import evaluar_movimiento
import time

TIME_WAIT = 1
RETRIES = 5


def procesar_lavado(nombre):
    print('PROCESANDO LAVADO DE MANOS')
    contador = True
    i = 0
    while contador:
        i += 1
        contador = False if i >= RETRIES else True

        if evaluar_movimiento():
            print('INICIANDO SECUENCIA DE LAVADO', nombre)
            secuencia_lavado(nombre)
            print('TERMINÓ SECUENCIA DE LAVADO', nombre)
            i = 0
            contador = False
        else:
            print('NO SE HA DETECTADO MOVIMIENTO')

        time.sleep(TIME_WAIT)

    return False if i >= RETRIES else True
