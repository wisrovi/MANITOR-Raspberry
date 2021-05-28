from flask import Flask
import csv
import io
from flask import make_response
import tablib

app = Flask(__name__)


@app.route('/')
def hola():
    return 'History by Wisrovi'


@app.route('/history')
def audio():
    f = str()
    try:
        with open("historico.csv", "r") as json_file:
            f = json_file.readlines()
            #data = json.load(f)
    except:
        print("error")

    contenido = list()
    title = '"ENVIADO","RECIBIDO"'
    contenido.append(title)
    for row in f:
        contenido.append(row)

    contenido_str = ""
    for lin in contenido:
        contenido_str += lin + "&"
    return contenido_str


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)