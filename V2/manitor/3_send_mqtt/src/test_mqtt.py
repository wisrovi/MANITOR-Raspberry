import paho.mqtt.client as mqtt  # import the client1

IP_BROKER = "192.168.1.115"
PORT_BROKER = "1883"
PORT_BROKER = int(PORT_BROKER)

print(f"Credenciales usar: ip={IP_BROKER} y port={PORT_BROKER}")


client_send = mqtt.Client("P1")
client_send.connect(IP_BROKER, port=PORT_BROKER)

import time

while True:
    time.sleep(5)
    print("publicando recursos")
    client_send.publish("/test_docker", "RPI")  # publish
