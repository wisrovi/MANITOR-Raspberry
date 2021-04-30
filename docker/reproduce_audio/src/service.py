from flask import Flask, request
import json
import os
from multiprocessing import Process

app = Flask(__name__)


def leer_audios_disponibles(FOLDER):
    audios_temporal = list()
    lista_audios = list()
    for fil in os.listdir(FOLDER):
        if os.path.isfile(os.path.join(FOLDER, fil)) and fil.endswith('.mp3'):
            lista_audios.append(fil)
    lista_audios = sorted(lista_audios)
    for fil in lista_audios:
        audios_temporal.append(os.path.join(FOLDER, fil))
    return audios_temporal


audios = leer_audios_disponibles("resources")


def reproducir_audio(i):
    os.system("mpg123 " + audios[i])


@app.route('/')
def hola():
    return 'Reproduce audio by Wisrovi'


@app.route('/audios')
def audio():
    OBJ = dict()
    for i, value in enumerate(audios):
        OBJ[str(i)] = value
    return json.dumps(OBJ, indent=4)


@app.route('/reproduce', methods=['GET'])
def reproduce():
    if len(audios) > 0:
        try:
            id = request.args.get('id')
            if id != '':
                id = int(id)
                print(id, type(id))
                if 0 <= id < len(audios):
                    Process(target=reproducir_audio, args=(id,)).start()
                    OBJ = dict()
                    OBJ['file'] = audios[id]
                    return json.dumps(OBJ, indent=4)
                else:
                    return "Valor de 'id' incorrecto"
            else:
                return "Valor de 'id' incorrecto"
        except:
            return 'Por favor verifique el envio de una variable llamada "id", si no conoce que valores puede tomar la variable consulte /audios'
    else:
        return "No hay audios para reproducir"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
