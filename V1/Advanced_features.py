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