import paho.mqtt.client as mqtt  # import the client1

broker_address = "192.168.1.112"
client_send = mqtt.Client("P1")
client_send.connect(broker_address, port=1885)


import time

while True:
    time.sleep(5)
    client_send.publish("/test_docker", "RPI")  # publish
