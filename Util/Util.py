
class Util(object):
    import json
    from Process.Mqtt.config_mqtt import FILE_MQTT
    from Process.Beacon_scan.config_beacon import NAME_FILE_BEACON

    def enviar_mqtt(self, uuid):
        OBJ = dict()
        OBJ['uuid'] = uuid
        with open(self.FILE_MQTT, 'w') as outfile:
            self.json.dump(OBJ, outfile)

    def read_data_scan_beacon(self):
        data = dict()
        with open(self.NAME_FILE_BEACON) as json_file:
            data = self.json.load(json_file)
        return data


