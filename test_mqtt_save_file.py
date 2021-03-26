import json
from Process.Mqtt.config_mqtt import FILE_MQTT

OBJ = dict()
OBJ['uuid'] = "1234567890abcdefghijklmnoprstuvwxyz"
with open(FILE_MQTT, 'w') as outfile:
    json.dump(OBJ, outfile)