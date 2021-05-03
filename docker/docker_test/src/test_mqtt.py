import paho.mqtt.client as mqtt  # import the client1

broker_address = "192.168.1.112"
client = mqtt.Client("P1")
client.connect(broker_address, port=1885)


import time

while True:
    time.sleep(5)
    client.publish("/test_docker", "RPI")  # publish
