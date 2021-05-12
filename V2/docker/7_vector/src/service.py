from flask import Flask, request, make_response
from datetime import datetime
import json
import requests


URL = 'http://localhost:5003/send?topic='


app = Flask(__name__)

VECTOR = dict()


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
    if not voltaje:
        voltaje = '3.7'

    enviar = []
    for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        if i in VECTOR:
            enviar.append(VECTOR[i])
        else:
            enviar.append(0)
    mensaje = '[' + ','.join([str(x) for x in enviar]) + ']'
    fecha = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    mensaje = '{' + str(voltaje) + ',' + str(fecha) + ',' + mensaje + '}'
    print(mensaje)
    envia_vector(mensaje)
    VECTOR = {}
    return make_response({'code': 'SUCESS'}, 200)


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    # options_config.append("reproduce audios")
    # options_config.append("id = numero del audio a reproducir")
    # options_config.append("la lista completa se puede ver en http://localhost:5002/audios")
    OBJ['http://localhost:5007/time?id=<id>'] = options_config

    options_config = list()
    # options_config.append("muestra audios")
    # options_config.append("Entrega un Json con toda la lista de audios a reproducir")
    OBJ['http://localhost:5007/report'] = options_config

    return json.dumps(OBJ, indent=4)


def envia_vector(mensaje):
    topic = '/holamundo'
    fullurl = URL + topic + '&msg=' + mensaje
    r = requests.get(url=fullurl)
    try:
        data = r.json()
        print(data)
    except:
        pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=True)
