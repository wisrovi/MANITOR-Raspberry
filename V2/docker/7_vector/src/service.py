from flask import Flask, request
import json

app = Flask(__name__)

VECTOR = list()

@app.route('/')
def hola():
    return 'Vector by Wisrovi'


@app.route('/time')
def time():
    global VECTOR
    OBJ = dict()
    pass

    pass
    return json.dumps(OBJ, indent=4)


@app.route('/report', methods=['GET'])
def report():
    return "No hay audios para reproducir"


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("reproduce audios")
    options_config.append("id = numero del audio a reproducir")
    options_config.append("la lista completa se puede ver en http://localhost:5002/audios")
    OBJ['http://localhost:5007/time?id=<id>'] = options_config

    options_config = list()
    options_config.append("muestra audios")
    options_config.append("Entrega un Json con toda la lista de audios a reproducir")
    OBJ['http://localhost:5007/report'] = options_config

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007)
