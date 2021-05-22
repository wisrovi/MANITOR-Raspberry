from flask import Flask, request, make_response
from datetime import datetime
import json
import requests
import os


SERVER = "localhost"
SERVER = "send_mqtt"


MAC_CLIENT = os.environ.get('MAC_CLIENT')
if MAC_CLIENT is None:
    MAC_CLIENT = ""

TOPIC_SEND_VECTOR = '/SPINPLM/'

URL_SERVICE_SEND_MQTT = 'http://' + SERVER + ':5003/send?topic='


app = Flask(__name__)


VECTOR = dict()


def envia_vector(mensaje, uuid, mac=None):
    if mac is None:
        mac = MAC_CLIENT
    topico = TOPIC_SEND_VECTOR + mac + "/" + uuid + "/lavado"
    fullurl = URL_SERVICE_SEND_MQTT + topico + '&msg=' + mensaje
    r = requests.get(url=fullurl)
    try:
        data = r.json()
        print(data)
    except:
        pass


@app.route('/')
def hola():
    return 'Vector by Wisrovi'


@app.route('/time')
def time():
    global VECTOR
    id = request.args.get('id')
    time = float(request.args.get('time'))
    if id and time:
        VECTOR[id] = time
        print(VECTOR)
        return make_response({'code': 'SUCESS'}, 200)
    else:
        return make_response({'code': 'NO DATA'}, 200)


@app.route('/report', methods=['GET'])
def report():
    global VECTOR

    voltaje = request.args.get('voltaje')
    uuid = request.args.get('uuid')
    mac = request.args.get('mac')
    if not voltaje:
        voltaje = '3.7'

    datos_vector_enviar = list()
    for i in range(10):
        if str(i) in VECTOR:
            datos_vector_enviar.append(VECTOR[str(i)])
        else:
            datos_vector_enviar.append(0)
    mensaje = '[' + ','.join([str(value_in_vector) for value_in_vector in datos_vector_enviar]) + ']'
    fecha = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    mensaje = '{' + str(voltaje) + ',' + str(fecha) + ',' + mensaje + '}'
    print(mensaje)
    envia_vector(mensaje, uuid, mac)
    VECTOR = dict()

    rta = dict()
    rta['data_send'] = mensaje
    rta['code'] = 'SUCESS'
    return make_response(rta, 200)


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("reproduce audios")
    options_config.append("id = posicion del vector a guardar")
    options_config.append("time = tiempo usado en esta posicion del vector")
    OBJ['http://localhost:5007/time?id=<id>&time=<time>'] = options_config

    options_config = list()
    options_config.append("<voltaje> recibe el voltaje del ibeacon para enviarlo al servidor")
    options_config.append("<uuid> recibe el uuid del beacon para enviarlo al servidor")
    options_config.append("<mac> recibe la mac del manitor para enviarlo al servidor")
    OBJ['http://localhost:5007/report?voltaje=<voltaje>&uuid=<uuid>&mac=<mac>'] = options_config

    return json.dumps(OBJ, indent=4)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=True)
