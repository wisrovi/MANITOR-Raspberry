from datetime import datetime
import time
from app.evaluar_movimiento import evaluar_movimiento
from app.get import get

pasos = {1: 8, 2: 5, 3: 8, 4: 7, 5: 9, 6: 6, 7: 5, 8: 8, 9: 9, 10: 9}

WAIT_TIME = 0.5 # 0.1
PENALITY_TIME = 3
CONTADOR = 30

URL_SONIDO = 'http://localhost:5002/reproduce?id='
URL_VIDEO = 'http://localhost:5005/mostrar?id=$ID&name='


def secuencia_lavado(nombre):
    proceso = True
    for paso in pasos:
        print('Inició lavado de manos paso:', paso, 'Actualizando audio y video')

        get(URL_SONIDO + str(paso))
        get(URL_VIDEO.replace('$ID', str(paso)) + nombre)
        hora = datetime.now()
        tiempo_estimado = 0.0 + pasos[paso]
        # print('Tiempo faltante', round(tiempo_estimado, 1), 'Segundos')
        contador = 0
        while tiempo_estimado > 0:
            time.sleep(WAIT_TIME)

            if contador >= CONTADOR:
                proceso = False
                break

            if evaluar_movimiento():
                contador = 0
            else:
                contador += 1
                if (contador % 6) == 0:
                    tiempo_estimado += PENALITY_TIME
                    print("Alerta: no hay movimiento")

            transcurrido = (datetime.now() - hora).total_seconds()
            hora = datetime.now()
            tiempo_estimado = tiempo_estimado - transcurrido

            # print('Tiempo faltante', round(tiempo_estimado, 1), 'Segundos')
        if not proceso:
            break

    return proceso
