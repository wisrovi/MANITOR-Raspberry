import time
from urls import URL_NAME, URL_ENVIA_VECTOR
from procesar_lavado import procesar_lavado
from get import get

salir = True
SLEEP_TIME = 5

contador = 0

while salir:
    # llamar al web service del nombre

    name_json = get(URL_NAME)
    # print(type(name_json))

    # COMENTAR CUANDO URL_NAME ESTE BIEN PARAMETRIZADO
    # name_text = '{ "fda50693-a4e2-4fb1-afcf-c6eb07647825": { "data": { "mac": "eb:ed:93:4a:db:b3", "rssi": -50, "uuid": "fda50693-a4e2-4fb1-afcf-c6eb07647825", "tx_power": 0, "major": 5, "minor": 6, "tipo": "iBeacon", "empresa": "fda50693" }, "name": "WilliamRodriguez", "time": "11/5/2021-13:28:44" } }'

    nombre = None

    if len(name_json) > 0:
        uuid = [f for f in name_json][0]
        name_json = name_json[uuid]
        print(name_json)
        if 'name' in name_json:
            nombre = name_json['name']
            print("[Debug]:", nombre)

            # if nombre != nombre_anterior:
            if not procesar_lavado(nombre):
                print('NO SE DETECTO MOVIMIENTO')
                # nombre_anterior = 'Fulano de Tal'
            else:
                print('ENVIANDO VECTOR')
                get(URL_ENVIA_VECTOR)
                # nombre_anterior = nombre
            # else:
            #     contador += 1

        # if contador >= 3:
        #     contador = 0
        #     nombre_anterior = 'Fulano de Tal'

    print('esperando 5 Segundos', nombre)

    time.sleep(SLEEP_TIME)
    # nombre_anterior = nombre

    # salir = False
