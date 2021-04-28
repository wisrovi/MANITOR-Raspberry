from Advanced_features import Orden_mqtt_recibida


class Mqtt(object):
    import paho.mqtt.client as mqtt
    import getmac
    import os
    from os import remove
    import json
    import datetime

    from Process.Mqtt.config_mqtt import BROKER_MQTT, PORT_MQTT, PROJECT, TOPICS_USAR, FILE_MQTT, PORT_MQTT_FCV, \
        BROKER_MQTT_FCV

    def __init__(self, clase_ejecutar):
        self.__get_mac()
        self.clase_ejecutar = clase_ejecutar

        self.client = self.mqtt.Client(self.IDENTIFICADOR_MANITOR)
        self.client.on_message = self.__on_message
        self.__conect()
        self.BASE_DIR = self.os.path.dirname(self.os.path.realpath(__file__))
        self.BASE_DIR_ROOT = "/".join([e for e in self.BASE_DIR.split("/")][:-2]) + "/"

    def __Leer_HoraActual(self):
        x = self.datetime.datetime.now()
        return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)

    def __get_mac(self):
        mac = self.getmac.get_mac_address()
        self.IDENTIFICADOR_MANITOR = mac

    def __exist_file(self, file):
        if self.os.path.isfile(file):
            return True
        else:
            return False

    def __conect(self):
        try:
            if self.__exist_file(self.BASE_DIR_ROOT + "FCV"):
                self.client.connect(host=self.BROKER_MQTT_FCV,
                                    port=self.PORT_MQTT_FCV)  # , keepalive=60, bind_address="") #connect to broker
                print("[main_mqtt]:", "usando broker FCV")
            else:
                self.client.connect(host=self.BROKER_MQTT,
                                    port=self.PORT_MQTT)  # , keepalive=60, bind_address="") #connect to broker
                print("[main_mqtt]:", "usando broker pruebas")
            for topic in self.TOPICS_USAR:
                self.__SuscribirTopic(topic)
                print("[main_mqtt]:", "Suscrito a:", topic)

            self.__IniciarEscuchaMQTT()
        except:
            print("[main_mqtt]:", "Error al conectarse al broker de MQTT")

    def EnviarCardHolder(self, uuid, vector_tiempos="[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"):
        mac = self.IDENTIFICADOR_MANITOR
        bateria = uuid[14:18]
        topic = self.PROJECT + "manitor/" + mac + "/" + uuid + "/lavado"
        msg = "{" + "'LV' : " + bateria + ", 'HOUR': " + self.__Leer_HoraActual() + ", 'vector_tiempos' : " + vector_tiempos + "}"
        self.EnviarDatoServidor(topic, msg)

    def EnviarDatoServidor(self, TOPIC_PUBLISH_MQTT, MENSAJE_ENVIAR_MQTT):
        self.client.publish(TOPIC_PUBLISH_MQTT, MENSAJE_ENVIAR_MQTT)  # publish

    def __SuscribirTopic(self, topic):
        self.client.subscribe(topic)

    def __on_message(self, client, userdata, message):
        topico = message.topic
        topico = topico.replace(self.PROJECT, "")
        mensaje = str(message.payload.decode("utf-8"))

        OTA = False
        if topico.find("OTA") >= 0:
            OTA = True

        RESTART = False
        if topico.find("restart") >= 0:
            RESTART = True

        if topico.find(self.IDENTIFICADOR_MANITOR) >= 0:
            if OTA:
                self.clase_ejecutar.private_ota()
            elif RESTART:
                self.clase_ejecutar.private_restart()
        else:
            if OTA:
                self.clase_ejecutar.public_ota()
            elif RESTART:
                self.clase_ejecutar.public_restart()

    def FinalizarEscuchaMQTT(self):
        self.client.loop_stop()  # stop the loop

    def __IniciarEscuchaMQTT(self):
        self.client.loop_start()

    def read_file(self):
        data = dict()
        FILE = self.BASE_DIR_ROOT + self.FILE_MQTT
        if self.os.path.isfile(FILE):
            with open(FILE) as json_file:
                data = self.json.load(json_file)
            self.remove(FILE)
        else:
            # print("no existe archivo mqtt", FILE)
            pass
        return data


if __name__ == "__main__":
    mqtt = Mqtt(Orden_mqtt_recibida)
    mqtt.EnviarDatoServidor("queso", "hola mundo")
