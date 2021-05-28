import paho.mqtt.client as mqtt  # import the client1


def on_message(client, userdata, message):
    DATA_RECEIVED = str(message.payload.decode("utf-8"))
    TOPIC_RECEIVED = message.topic

    OBJ = dict()
    OBJ['topic'] = TOPIC_RECEIVED
    OBJ['sms'] = DATA_RECEIVED
    print(OBJ)


IP_BROKER = "192.168.1.115"
PORT_BROKER = "1883"



# IP_BROKER = "172.30.19.92"
# PORT_BROKER = "1883"






PORT_BROKER = int(PORT_BROKER)

print(f"Credenciales usar: ip={IP_BROKER} y port={PORT_BROKER}")

client_receive = mqtt.Client("P2")

client_receive.on_message=on_message

client_receive.connect(IP_BROKER, port=PORT_BROKER)




client_receive.subscribe("/#")



client_receive.loop_start()


client_receive.publish("/house/bulbs/bulb1","OFF")


import time
while True:
    time.sleep(5)
    print(".", end="")

# time.sleep(30) # wait
# client_receive.loop_stop()
