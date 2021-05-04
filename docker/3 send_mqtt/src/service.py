import time

from flask import Flask, request
import json
import os
import random
from multiprocessing import Process
import paho.mqtt.client as mqtt  # import the client1
import getmac
import datetime

IP_BROKER = os.environ.get('IP_BROKER')
PORT_BROKER = os.environ.get('PORT_BROKER')
NAME_CLIENT = os.environ.get('NAME_CLIENT')
MAC_CLIENT = os.environ.get('MAC_CLIENT')
USER_BROKER = os.environ.get('USER')
PASSWORD_BROKER = os.environ.get('PASSWORD')

DATA_RECEIVED = str()
TOPIC_RECEIVED = str()
TIME_RECEIVED = str()

print("IP_BROKER", IP_BROKER)
print("PORT_BROKER", PORT_BROKER)
print("NAME_CLIENT", NAME_CLIENT)
print("MAC_CLIENT", MAC_CLIENT)
print("USER_BROKER", USER_BROKER)
print("PASSWORD_BROKER", PASSWORD_BROKER)


def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


def get_mac():
    mac = getmac.get_mac_address()
    return MAC_CLIENT


def on_message(client, userdata, message):
    global DATA_RECEIVED
    global TOPIC_RECEIVED
    global TIME_RECEIVED
    DATA_RECEIVED = str(message.payload.decode("utf-8"))
    TOPIC_RECEIVED = message.topic
    TIME_RECEIVED = Leer_HoraActual()
    # print("message received ", DATA_RECEIVED)
    # print("message topic=", message.topic)
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)


def on_connect_received(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO]: connected OK Returned code=", rc)
    elif rc == 1:
        print("[INFO]: Conexión rechazada - versión de protocolo incorrecta")
    elif rc == 2:
        print("[INFO]: Conexión rechazada: identificador de cliente no válido")
    elif rc == 3:
        print("[INFO]: Conexión rechazada - servidor no disponible")
    elif rc == 4:
        print("[INFO]: Conexión rechazada - nombre de usuario o contraseña incorrectos")
    elif rc == 5:
        print("[INFO]: Conexión rechazada - no autorizada")
    else:
        print("[ERROR]: Bad connection Returned code=", rc)
    print()


def on_connect_send(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO]: connected OK Returned code=", rc)
    elif rc == 1:
        print("[INFO]: Conexión rechazada - versión de protocolo incorrecta")
    elif rc == 2:
        print("[INFO]: Conexión rechazada: identificador de cliente no válido")
    elif rc == 3:
        print("[INFO]: Conexión rechazada - servidor no disponible")
    elif rc == 4:
        print("[INFO]: Conexión rechazada - nombre de usuario o contraseña incorrectos")
    elif rc == 5:
        print("[INFO]: Conexión rechazada - no autorizada")
    else:
        print("[ERROR]: Bad connection Returned code=", rc)
    print()


def send_msg_mqtt(topic, msg):
    print(f"[MQTT]: topic:{topic} - message:{msg}")
    client_send.publish(topic, msg)  # publish


def conectar_broker():
    global conectado
    try:
        client_receive.on_connect = on_connect_received

        if USER_BROKER is not None and PASSWORD_BROKER is not None:
            print("Usando user y password")
            client_receive.username_pw_set(username=USER_BROKER, password=PASSWORD_BROKER)
            client_send.username_pw_set(username=USER_BROKER, password=PASSWORD_BROKER)

        client_receive.connect(IP_BROKER, port=int(PORT_BROKER))
        client_send.connect(IP_BROKER, port=int(PORT_BROKER))

        PROJECT = "SPINPLM"
        topic_subscribe_1 = "/" + PROJECT + "/manitor/#"
        topic_subscribe_2 = topic_subscribe_1[:-1] + get_mac() + "/#"

        client_receive.subscribe(topic_subscribe_1, qos=1)
        client_receive.subscribe(topic_subscribe_2, qos=1)

        print("subscrito a:", topic_subscribe_1)
        print("subscrito a:", topic_subscribe_2)
        print()

        client_receive.on_message = on_message
        client_receive.loop_start()

        conectado = True

        Process(target=send_msg_mqtt, args=("/" + MAC_CLIENT, "Hello world",)).start()
    except:
        print("Credenciales no validas")


def on_disconnect_receive(client, userdata, rc):
    print("[ERROR]: disconnecting reason  " + str(rc))
    client.loop_stop()
    time.sleep(5)
    conectar_broker()

def on_disconnect_send(client, userdata, rc):
    print("[ERROR]: disconnecting reason  " + str(rc))
    client.loop_stop()
    time.sleep(5)
    conectar_broker()


conectado = False
if IP_BROKER is None or PORT_BROKER is None or NAME_CLIENT is None:
    print("No hay credenciales para conectar al broker")
else:
    char = "abcdefghijklmnñopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    NAME_CLIENT = str()
    for _ in range(10):
        NAME_CLIENT = NAME_CLIENT + random.choice(char)
    os.environ['NAME_CLIENT'] = NAME_CLIENT

    client_receive = mqtt.Client(NAME_CLIENT, clean_session=False)
    client_send = mqtt.Client(NAME_CLIENT + "2", clean_session=False)
    client_receive.on_disconnect = on_disconnect_receive
    client_send.on_disconnect = on_disconnect_send
    conectar_broker()


def continue_life_pin():
    while True:
        Process(target=send_msg_mqtt, args=("/" + MAC_CLIENT, "life_pin",)).start()
        time.sleep(60)


Process(target=continue_life_pin).start()

app = Flask(__name__)


@app.route('/')
def hola():
    return 'Send MQTT by Wisrovi'


@app.route('/data')
def data():
    OBJ = dict()
    OBJ['data'] = DATA_RECEIVED
    OBJ['topic'] = TOPIC_RECEIVED
    OBJ['time_received'] = TIME_RECEIVED
    return json.dumps(OBJ, indent=4)


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
        conectar_broker()
    return json.dumps(OBJ, indent=4)


@app.route('/send', methods=['POST', 'GET'])
def send():
    if conectado:
        if request.method == 'POST':
            msg = request.form['msg']
            topic = request.form['topic']
        else:
            msg = request.args.get('msg')
            topic = request.args.get('topic')
        # topic = str(topic.replace("'", ""))
        # topic = topic[topic.find("/"):]

        print()
        print("***************************************************************************")
        print(topic, " -> ", msg)

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

    options_config = list()
    options_config.append("look data received")
    options_config.append("look topic received")
    options_config.append("( /SPINPLM/manitor/# )")
    options_config.append("( /SPINPLM/manitor/<mac-raspberry>/# )")
    OBJ['http://localhost:5003/data'] = options_config

    options_send = list()
    options_send.append("<topic> -> topico enviar mqtt")
    options_send.append("<msg> -> mensaje enviar mqtt")
    OBJ['http://localhost:5003/send?topic=<topic>&msg=<msg>'] = options_send

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
