from config_beacon import TIME_SCAN

from flask import Flask
app = Flask(__name__)

import json
import time


from ScanUtility import beacontools


PRINT_LOG = True
scan_beacon = beacontools(0, TIME_SCAN)
scan_beacon.start_continue_process()


@app.route('/beacons')
def hello():
    BEACONS = scan_beacon.get_beacons()
    DATOS = dict()
    for key, beacon_class in BEACONS.items():
        DATOS[key] = beacon_class.getJson()
    data_beacons_json = json.dumps(DATOS, indent=4)
    rta = data_beacons_json
    # print(rta)
    return rta


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("look beacons now")
    options_config.append("it is recommended to consult every 5 seconds")
    OBJ['http://localhost:5001/beacons'] = options_config

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
