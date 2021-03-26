from MqttUtil import Mqtt
import time


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


class Mqtt_Decorador(object):
    def __init__(self, name, mqtt):
        self.name = name
        self.mqtt = mqtt

    def __call__(self, f):
        def none(*args, **kw_args):
            print(self.name)
            rta = f(*args, **kw_args)
            self.mqtt.FinalizarEscuchaMQTT()
            return rta

        return none


mqtt = Mqtt(Orden_mqtt_recibida)


@Mqtt_Decorador("mqtt manitor", mqtt)
def main_mqtt():
    while True:
        time.sleep(3)
        data = mqtt.read_file()
        if len(data) > 0:
            print(data)
            mqtt.EnviarCardHolder(data['uuid'])
    mqtt.FinalizarEscuchaMQTT()


if __name__ == "__main__":
    main_mqtt()
