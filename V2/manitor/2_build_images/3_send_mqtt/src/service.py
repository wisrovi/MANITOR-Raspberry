USAR_DOS_CLIENTES = True

import time

from flask import Flask, request
import json
import os
import random
from multiprocessing import Process
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import datetime

FILE_SAVE_CONFIG = "config.json"
PROJECT = "SPINPLM"

TOPIC_SUBSCRIBE = list()

IP_BROKER = os.environ.get('IP_BROKER')
PORT_BROKER = os.environ.get('PORT_BROKER')
NAME_CLIENT = os.environ.get('NAME_CLIENT')
MAC_CLIENT = os.environ.get('MAC_CLIENT')
USER_BROKER = os.environ.get('USER')
PASSWORD_BROKER = os.environ.get('PASSWORD')

DATA_RECEIVED = str()
TOPIC_RECEIVED = str()
TIME_RECEIVED = str()
NOMBRE = str()
OTA = False
restart = False

print("[environ]: IP_BROKER", IP_BROKER)
print("[environ]: PORT_BROKER", PORT_BROKER)
print("[environ]: NAME_CLIENT", NAME_CLIENT)
print("[environ]: MAC_CLIENT", MAC_CLIENT)
print("[environ]: USER_BROKER", USER_BROKER)
print("[environ]: PASSWORD_BROKER", PASSWORD_BROKER)
print()

client_receive = None
client_send = None


def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


def get_mac():
    return MAC_CLIENT


def on_message(client, userdata, message):
    global DATA_RECEIVED
    global TOPIC_RECEIVED
    global TIME_RECEIVED
    global NOMBRE
    global OTA
    global restart

    DATA_RECEIVED = str(message.payload.decode("utf-8"))
    TOPIC_RECEIVED = message.topic
    TIME_RECEIVED = Leer_HoraActual()

    filter_base = "/" + PROJECT + "/manitor/"
    filter_topic = filter_base + MAC_CLIENT + "/"

    restore_filter = TOPIC_RECEIVED[len(filter_topic):]
    restore_filter_2 = TOPIC_RECEIVED[len(filter_base):]

    print("[received]: [topic base]:", filter_topic)
    print("[received]: [topic complete]:", TOPIC_RECEIVED)
    print("[received]: [filter]:", restore_filter)
    print("[received]: [mac]:", MAC_CLIENT)
    print("[received]: [mensaje]:", DATA_RECEIVED)
    if restore_filter == "nombre":
        NOMBRE = DATA_RECEIVED
        print("[received]: [nombre]:", NOMBRE)

    if restore_filter == "OTA":
        OTA = True
        print("[received]: [OTA]:", OTA)

    if restore_filter == "restart":
        restart = True
        print("[received]: [restart]:", restart)

    if restore_filter_2 == "OTA":
        OTA = True
        print("[received]: [OTA]:", OTA)

    if restore_filter_2 == "restart":
        restart = True
        print("[received]: [restart]:", restart)
    print()

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
    if USAR_DOS_CLIENTES:
        if client_send is not None:
            client_send.publish(topic, msg)  # publish
            print("[MQTT send]: OK")
        else:
            OBJ = dict()
            try:
                with open(FILE_SAVE_CONFIG) as json_file:
                    OBJ = json.load(json_file)
            except:
                pass

            if len(OBJ) > 0:
                ip = OBJ['ip']
                port = OBJ['port']
                name = OBJ['name']

                user = OBJ.get('user')
                password = OBJ.get('password')

                data_auth = None
                if user is not None and password is not None:
                    data_auth = {
                        'username': user,
                        'password': password
                    }

                try:
                    publish.single(topic, payload=msg,
                                   hostname=ip, port=int(port), client_id=name,
                                   auth=data_auth)
                except:
                    print("[MQTT send]: BAD")


def conectar_broker():
    global conectado
    global client_receive
    global client_send
    global PORT_BROKER
    global TOPIC_SUBSCRIBE

    if MAC_CLIENT is None:
        print("[conection]: No hay MAC para susbcribirse")

    PORT_BROKER = int(PORT_BROKER)

    char = "abcdefghijklmnñopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    NAME_CLIENT = str()
    for _ in range(10):
        NAME_CLIENT = NAME_CLIENT + random.choice(char)
    os.environ['NAME_CLIENT'] = NAME_CLIENT

    print("[conection]: Nombre cliente receptor:", NAME_CLIENT)
    client_receive = mqtt.Client(NAME_CLIENT)

    client_receive.on_message = on_message
    client_receive.on_connect = on_connect_received
    client_receive.on_disconnect = on_disconnect_receive

    NAME_CLIENT = NAME_CLIENT + "2"

    if USAR_DOS_CLIENTES:
        print("[conection]: Nombre cliente transmision:", NAME_CLIENT)
        client_send = mqtt.Client(NAME_CLIENT, clean_session=False)

        client_send.on_disconnect = on_disconnect_send

    try:
        if client_receive is None:
            print("[conection]: Error creando cliente para recepcion")

        if USAR_DOS_CLIENTES:
            if client_send is None:
                print("[conection]: Error creando cliente para transmision")

        if USER_BROKER is not None and PASSWORD_BROKER is not None:
            print("Usando user y password")
            client_receive.username_pw_set(username=USER_BROKER, password=PASSWORD_BROKER)
            if USAR_DOS_CLIENTES:
                client_send.username_pw_set(username=USER_BROKER, password=PASSWORD_BROKER)

        print("[conection]: conectando al broker para recepcion")
        print(f"[conection]: Credenciales usar: ip={IP_BROKER} y port={PORT_BROKER}")
        client_receive.connect(IP_BROKER, port=PORT_BROKER)

        if USAR_DOS_CLIENTES:
            print("[conection]: conectando al broker para publicar")
            client_send.connect(IP_BROKER, port=int(PORT_BROKER))

        print("[conection]: creando topics para subscripcion")
        topic_subscribe_1 = "/" + PROJECT + "/manitor/OTA"
        topic_subscribe_2 = "/" + PROJECT + "/manitor/restart"
        topic_subscribe_5 = "/" + PROJECT + "/manitor/" + MAC_CLIENT + "/nombre"
        topic_subscribe_3 = "/" + PROJECT + "/manitor/" + MAC_CLIENT + "/OTA"
        topic_subscribe_4 = "/" + PROJECT + "/manitor/" + MAC_CLIENT + "/restart"
        print("[conection]: Subscribiendo a ", topic_subscribe_1)
        print("[conection]: Subscribiendo a ", topic_subscribe_2)
        print("[conection]: Subscribiendo a ", topic_subscribe_3)
        print("[conection]: Subscribiendo a ", topic_subscribe_4)
        print("[conection]: Subscribiendo a ", topic_subscribe_5)
        client_receive.subscribe(topic_subscribe_1)
        client_receive.subscribe(topic_subscribe_2)
        client_receive.subscribe(topic_subscribe_3)
        client_receive.subscribe(topic_subscribe_4)
        client_receive.subscribe(topic_subscribe_5)
        print("[conection]: subscrito a:", topic_subscribe_1)
        print("[conection]: subscrito a:", topic_subscribe_2)
        print("[conection]: subscrito a:", topic_subscribe_3)
        print("[conection]: subscrito a:", topic_subscribe_4)
        print("[conection]: subscrito a:", topic_subscribe_5)

        print("[conection]: iniciando bucle infinito de recepcion")
        print()
        client_receive.loop_start()

        conectado = True

        Process(target=send_msg_mqtt, args=("/" + MAC_CLIENT, "Hello world",)).start()
        print()

        TOPIC_SUBSCRIBE.append(topic_subscribe_1)
        TOPIC_SUBSCRIBE.append(topic_subscribe_2)
        TOPIC_SUBSCRIBE.append(topic_subscribe_3)
        TOPIC_SUBSCRIBE.append(topic_subscribe_4)
        TOPIC_SUBSCRIBE.append(topic_subscribe_5)
    except:
        print("[conection]: Credenciales no validas")
        print()


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

OBJ = dict()
existe_archivo_configuracion = False
try:
    with open(FILE_SAVE_CONFIG) as json_file:
        OBJ = json.load(json_file)
    existe_archivo_configuracion = True
except:
    pass

if existe_archivo_configuracion:
    IP_BROKER = OBJ.get("ip")
    PORT_BROKER = OBJ.get("port")
    NAME_CLIENT = OBJ.get("name")
    MAC_CLIENT = OBJ.get("mac")
    USER_BROKER = OBJ.get("user")
    PASSWORD_BROKER = OBJ.get("password")
    print("[config]: cargando configuración guardada en el archivo config.json")
    print()

if IP_BROKER is None or PORT_BROKER is None or NAME_CLIENT is None:
    print("[conection]: No hay credenciales para conectar al broker")
    print()
else:
    conectar_broker()


def continue_life_pin():
    mac = MAC_CLIENT
    while True:
        if mac is None:
            OBJ = dict()
            try:
                with open(FILE_SAVE_CONFIG) as json_file:
                    OBJ = json.load(json_file)
                    mac = OBJ['mac']
            except:
                pass

        if mac is not None:
            Process(target=send_msg_mqtt, args=("/" + mac, "life_pin",)).start()
            print("[mqtt send lifePin]: Enviado pin de vida")
        else:
            print("[mqtt send lifePin]: Error")
        time.sleep(60)


Process(target=continue_life_pin).start()

app = Flask(__name__)


@app.route('/')
def hola():
    return 'Send MQTT by Wisrovi'


@app.route('/mac')
def mac():
    return MAC_CLIENT


@app.route('/topics')
def topics():
    OBJ = dict()
    for key, value in enumerate(TOPIC_SUBSCRIBE):
        OBJ[str(key)] = value
    return json.dumps(OBJ, indent=4)


@app.route('/credenciales')
def credenciales():
    OBJ = dict()
    OBJ['ip'] = IP_BROKER
    OBJ['port'] = PORT_BROKER
    OBJ['name_client'] = NAME_CLIENT
    return json.dumps(OBJ, indent=4)


@app.route('/data')
def data():
    global NOMBRE
    OBJ = dict()
    OBJ['data'] = DATA_RECEIVED
    OBJ['topic'] = TOPIC_RECEIVED
    OBJ['nombre'] = NOMBRE
    OBJ['OTA'] = OTA
    OBJ['restart'] = restart
    OBJ['time_received'] = TIME_RECEIVED

    NOMBRE = str()
    return json.dumps(OBJ, indent=4)


@app.route('/config')
def config():
    global NAME_CLIENT
    global IP_BROKER
    global PORT_BROKER
    global USER_BROKER
    global PASSWORD_BROKER
    global MAC_CLIENT
    global conectado

    port = request.args.get('port')
    ip = request.args.get('ip')
    name = request.args.get('name')
    user = request.args.get('user')
    pwd = request.args.get('pwd')
    mac = request.args.get('mac')

    if ip is not None:
        os.environ['IP_BROKER'] = ip
        IP_BROKER = ip
        print("[save new config]: new ip broker")

    if port is not None:
        os.environ['PORT_BROKER'] = port
        PORT_BROKER = port
        print("[save new config]: new port broker")

    if name is not None:
        os.environ['NAME_CLIENT'] = name
        NAME_CLIENT = name
        print("[save new config]: new name client for broker")

    if user is not None:
        os.environ['USER_BROKER'] = user
        USER_BROKER = user
        print("[save new config]: new user broker")

    if pwd is not None:
        os.environ['PASSWORD_BROKER'] = pwd
        PASSWORD_BROKER = pwd
        print("[save new config]: new password broker")

    if mac is not None:
        os.environ['MAC_CLIENT'] = mac
        MAC_CLIENT = mac
        print("[save new config]: new mac client")

    print()

    OBJ = dict()
    OBJ['ip'] = IP_BROKER
    OBJ['port'] = PORT_BROKER
    OBJ['name'] = NAME_CLIENT
    OBJ['mac'] = MAC_CLIENT

    if USER_BROKER is not None and PASSWORD_BROKER is not None:
        OBJ['user'] = USER_BROKER
        OBJ['password'] = PASSWORD_BROKER

    with open(FILE_SAVE_CONFIG, 'w') as outfile:
        json.dump(OBJ, outfile)

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
        print("[send from get to mqtt]: sending")
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
    options_config.append("look: port_broker")
    options_config.append("look: ip_broker")
    options_config.append("look: user_broker")
    options_config.append("look: password_broker")
    options_config.append("look: name_client_conect_broker")
    options_config.append("look: mac_client")
    OBJ['http://localhost:5003/config'] = options_config

    options_config = list()
    options_config.append("config: ip broker")
    options_config.append("config: port broker")
    options_config.append("config: user_broker")
    options_config.append("config: password_broker")
    options_config.append("config: name_client_conect_broker")
    options_config.append("config: mac client")
    OBJ[
        'http://localhost:5003/config?ip=<ip broker>&port=<port broker>&name=<name client>&mac=<mac client>&user=<user broker [optional]>&&pwd=<password broker [optional]>'] = options_config

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

    options_send = list()
    options_send.append("ver credenciales de conexion")
    OBJ['http://localhost:5003/credenciales'] = options_send

    options_send = list()
    options_send.append("ver mac de conexion del cliente")
    OBJ['http://localhost:5003/mac'] = options_send

    options_send = list()
    options_send.append("ver topics de conexion del cliente al broker")
    OBJ['http://localhost:5003/topics'] = options_send

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
