from flask import Flask, request
import json
import os
import random
from multiprocessing import Process
import paho.mqtt.client as mqtt  # import the client1


IP_BROKER = os.environ.get('IP_BROKER')
PORT_BROKER = os.environ.get('PORT_BROKER')
NAME_CLIENT = os.environ.get('NAME_CLIENT')


print("IP_BROKER", IP_BROKER)
print("PORT_BROKER", PORT_BROKER)
print("NAME_CLIENT", NAME_CLIENT)


conectado = False
if IP_BROKER is None or PORT_BROKER is None or NAME_CLIENT is None:
    print("No hay credenciales para conectar al broker")
else:
    char = "abcdefghijklmnñopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    NAME_CLIENT = str()
    for _ in range(10):
        NAME_CLIENT = NAME_CLIENT + random.choice(char)
    os.environ['NAME_CLIENT'] = NAME_CLIENT

    client = mqtt.Client(NAME_CLIENT)
    try:
        client.connect(IP_BROKER, port=int(PORT_BROKER))
        conectado = True
    except:
        print("Credenciales no validas")

app = Flask(__name__)


def send_msg_mqtt(topic, msg):
    client.publish(topic, msg)  # publish


@app.route('/')
def hola():
    return 'Send MQTT by Wisrovi'


@app.route('/config')
def config():
    global NAME_CLIENT
    global IP_BROKER
    global PORT_BROKER
    global conectado

    port = request.args.get('port')
    ip = request.args.get('ip')
    name = request.args.get('name')

    if ip is not None:
        os.environ['IP_BROKER'] = ip
        IP_BROKER = ip

    if port is not None:
        os.environ['PORT_BROKER'] = port
        PORT_BROKER = port

    if name is not None:
        os.environ['NAME_CLIENT'] = name
        NAME_CLIENT = name

    OBJ = dict()
    OBJ['ip'] = IP_BROKER
    OBJ['port'] = PORT_BROKER
    OBJ['name'] = NAME_CLIENT

    if not conectado:
        try:
            client.connect(IP_BROKER, port=int(PORT_BROKER))
            conectado = True
        except:
            print("Credenciales no validas")
    return json.dumps(OBJ, indent=4)


@app.route('/send', methods=['GET'])
def send():
    if conectado:
        msg = request.args.get('msg')
        topic = request.args.get('topic')
        if msg is not None and topic is not None:
            OBJ = dict()
            OBJ['topic'] = topic
            OBJ['msg'] = msg

            Process(target=send_msg_mqtt, args=(topic, msg,)).start()

            return json.dumps(OBJ, indent=4)
        else:
            return "Faltan variables de 'msg' y 'topic'"
    else:
        return "No se han configurado credenciales correctas, por favor use '/config' (mas ayuda en  http://localhost:5003/help)"


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("look port_broker")
    options_config.append("look ip_broker")
    OBJ['http://localhost:5003/config'] = options_config

    options_send = list()
    options_send.append("<topic> -> topico enviar mqtt")
    options_send.append("<msg> -> mensaje enviar mqtt")
    OBJ['http://localhost:5003/send?topic=<topic>&msg=<msg>'] = options_send

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
