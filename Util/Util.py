
class Util(object):
    import json
    from Process.Mqtt.config_mqtt import FILE_MQTT

    def enviar_mqtt(self, uuid):
        OBJ = dict()
        OBJ['uuid'] = uuid
        with open(self.FILE_MQTT, 'w') as outfile:
            self.json.dump(OBJ, outfile)


