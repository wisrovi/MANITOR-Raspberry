import paho.mqtt.client as mqtt  # import the client1
import json


from datetime import datetime

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{}/{}/{}-{}:{}:{}".format(day, month, year, date.hour, date.minute, date.second)
    return messsage

def get_date_time():
    now = datetime.now()
    data_date = current_date_format(now)
    return data_date



datos_recibidos = list()



def on_message(client, userdata, message):
    global datos_recibidos
    DATA_RECEIVED = str(message.payload.decode("utf-8"))
    TOPIC_RECEIVED = message.topic

    OBJ = dict()
    OBJ['topic'] = TOPIC_RECEIVED
    OBJ['sms'] = DATA_RECEIVED
    OBJ['time'] = get_date_time()#"hora-recibido"

    datos_recibidos.append(OBJ)


#IP_BROKER = "192.168.1.112"
#PORT_BROKER = "1884"



IP_BROKER = "172.30.19.92"
PORT_BROKER = "1883"






PORT_BROKER = int(PORT_BROKER)

print(f"Credenciales usar: ip={IP_BROKER} y port={PORT_BROKER}")

client_receive = mqtt.Client("P2")

client_receive.on_message=on_message

client_receive.connect(IP_BROKER, port=PORT_BROKER)




client_receive.subscribe("/SPINPLM/manitor/b8:27:eb:70:fd:71/nombre")



client_receive.loop_start()


intercalador = False
import time
while True:
    print(".", end="")        
    
    if len(datos_recibidos) > 0:
        data_received = dict()
        for id, value in enumerate(datos_recibidos):
            data_received[str(id)] = value

        data = json.dumps(data_received)
        with open("historico.csv", "a") as file:
            file.write(data)
        
    datos_recibidos = list()    

    intercalador = False if intercalador else True
    if intercalador:
        topico_enviar = "/SPINPLM/manitor/b8:27:eb:70:fd:71/fda50693-a4e2-4fb1-afcf-c6eb07647825/solicitud"
    else:
        topico_enviar = "/SPINPLM/manitor/b8:27:eb:70:fd:71/00007067-8690-e202-8d7b-203206310317/solicitud"


    mensaje_enviar = "1"

    OBJ = dict()
    OBJ['topic'] = topico_enviar
    OBJ['sms'] = mensaje_enviar
    OBJ['time'] = get_date_time()#"hora-enviar"

    data = json.dumps(OBJ)
    print(data)

    client_receive.publish(topico_enviar, mensaje_enviar)

    with open("historico.csv", "a") as file:
        file.write('\n' + data + ",")

    time.sleep(5)

# time.sleep(30) # wait
# client_receive.loop_stop()