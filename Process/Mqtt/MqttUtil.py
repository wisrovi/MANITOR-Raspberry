class Mqtt(object):
    import paho.mqtt.client as mqtt
    import getmac
    import os
    from os import remove
    import json
    import datetime

    from Process.Mqtt.config_mqtt import BROKER_MQTT, PORT_MQTT, PROJECT, TOPICS_USAR, FILE_MQTT

    def __init__(self, clase_ejecutar):
        self.__get_mac()
        self.clase_ejecutar = clase_ejecutar

        self.client = self.mqtt.Client(self.IDENTIFICADOR_MANITOR)
        self.client.on_message = self.__on_message
        self.__conect()

    def __Leer_HoraActual(self):
        x = self.datetime.datetime.now()
        return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)

    def __get_mac(self):
        mac = self.getmac.get_mac_address()
        self.IDENTIFICADOR_MANITOR = mac

    def __conect(self):
        try:
            self.client.connect(host=self.BROKER_MQTT,
                                port=self.PORT_MQTT)  # , keepalive=60, bind_address="") #connect to broker
            for topic in self.TOPICS_USAR:
                self.__SuscribirTopic(topic)
                print("Suscrito a:", topic)

            self.__IniciarEscuchaMQTT()
        except:
            print("Error al conectarse al broker de MQTT")

    def EnviarCardHolder(self, uuid):
        mac = self.IDENTIFICADOR_MANITOR
        bateria = uuid[14:18]
        topic = self.PROJECT + "manitor/" + mac + "/" + uuid
        msg = "{" + "'LV' : " + bateria + ", 'HOUR': " + self.__Leer_HoraActual() + ", 'mac' : " + mac + "}"
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
        FILE = "../../" + self.FILE_MQTT
        if self.os.path.isfile(FILE):
            with open(FILE) as json_file:
                data = self.json.load(json_file)
            self.remove(FILE)
        return data


if __name__ == "__main__":
    class Orden_mqtt_recibida:
        @staticmethod
        def public_ota():
            print("Orden publica: OTA")

        @staticmethod
        def public_restart():
            print("Orden publica: restart")

        @staticmethod
        def private_ota():
            print("Orden privada: OTA")

        @staticmethod
        def private_restart():
            print("Orden privada: restart")


    mqtt = Mqtt(Orden_mqtt_recibida)
    mqtt.EnviarDatoServidor("queso", "hola mundo")
