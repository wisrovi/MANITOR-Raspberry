import requests
from flask import Flask, request
import json
import os
import datetime
import getmac
import time
from multiprocessing import Process

SERVER = "localhost"


FILE_HISTORY = "DATA/history.json"
FILE_BEACON_SCAN = "/code/DATA/BEACON_SCAN.json"
FILE_PERSON_SCAN = "DATA/PERSON_SCAN.json"

PERSON_SCAN = dict()
PERSON_SCAN_NOW = dict()


def save_file(PERSON_SCAN_TEMP):
    with open(FILE_HISTORY, 'w') as outfile:
        json.dump(PERSON_SCAN_TEMP, outfile)


def read_file():
    PERSON_SCAN_TEMP = dict()
    try:
        with open(FILE_HISTORY) as json_file:
            PERSON_SCAN_TEMP = json.load(json_file)
    except:
        pass
    return PERSON_SCAN_TEMP


if not os.path.isfile(FILE_HISTORY):
    with open(FILE_HISTORY, 'w') as outfile:
        json.dump({}, outfile)
else:
    PERSON_SCAN = read_file()

if not os.path.isfile(FILE_BEACON_SCAN):
    with open(FILE_BEACON_SCAN, 'w') as outfile:
        json.dump({}, outfile)

if not os.path.isfile(FILE_PERSON_SCAN):
    with open(FILE_PERSON_SCAN, 'w') as outfile:
        json.dump({}, outfile)


app = Flask(__name__)


def Leer_HoraActual():
    x = datetime.datetime.now()
    return "{}/{}/{}".format(x.day, x.month, x.year) + "-" + "{}:{}:{}".format(x.hour, x.minute, x.second)


def get_mac():
    mac = getmac.get_mac_address()
    return mac


def get_topic(uuid):
    PROJECT = "SPINPLM"
    topic = "/" + PROJECT + "/manitor/" + get_mac() + "/" + uuid + "/solicitud"
    return topic


def get_beacons_scan():
    global PERSON_SCAN
    global PERSON_SCAN_NOW
    while True:
        time.sleep(4.5)
        PARAMS = dict()
        failed = False
        BEACON_SCAN_FILE = None
        try:
            r = requests.get('http://' + SERVER + ':5001/beacons', params=PARAMS, timeout=10)
            BEACON_SCAN_FILE = r.json()
        except:
            print("[ERROR]: Problema al enviar el dato al servidor (port: 5001)")
            failed = True

        if not failed:
            more_near_rssi = dict()
            for key, value in BEACON_SCAN_FILE.items():
                more_near_rssi[key] = value['rssi']
            more_near_sorted = {k: v for k, v in sorted(more_near_rssi.items(), key=lambda item: item[1], reverse=True)}

            MORE_NEAR = dict()
            for k, v in more_near_sorted.items():
                MORE_NEAR[k] = BEACON_SCAN_FILE[k]
                break

            OBJ = dict()
            OBJ['all'] = BEACON_SCAN_FILE
            OBJ['near'] = MORE_NEAR
            with open(FILE_BEACON_SCAN, 'w') as outfile_beacon_scan:
                json.dump(OBJ, outfile_beacon_scan)

            print(MORE_NEAR)

            all_uuid = list(MORE_NEAR.keys())
            if len(all_uuid) > 0:
                uuid_mas_cercano = list(MORE_NEAR.keys())[0]
                PARAMS = dict()
                PARAMS['msg'] = "1"
                PARAMS['topic'] = get_topic(uuid_mas_cercano)
                r = requests.post('http://' + SERVER + ':5003/send', data=PARAMS, timeout=10)
                # print(r.text, PARAMS['topic'])

                time.sleep(0.5)
                PARAMS = dict()
                r = requests.get('http://' + SERVER + ':5003/data', params=PARAMS, timeout=10)
                data_response = r.json()
                # print(data_response['data'])

                if len(data_response['data'])>0:
                    OBJ = dict()
                    OBJ['data'] = MORE_NEAR[uuid_mas_cercano]
                    OBJ['name'] = data_response['data']
                    OBJ['time'] = Leer_HoraActual()

                    if not uuid_mas_cercano in list(PERSON_SCAN.keys()):
                        PERSON_SCAN[uuid_mas_cercano] = OBJ
                        save_file(PERSON_SCAN)

                    PERSON_SCAN_NOW = dict()
                    PERSON_SCAN_NOW[uuid_mas_cercano] = OBJ
                    with open(FILE_PERSON_SCAN, 'w') as outfile_beacon_scan:
                        json.dump(PERSON_SCAN_NOW, outfile_beacon_scan)
                else:
                    print("[ERROR]:", f"La persona con beacon {uuid_mas_cercano} no tiene resultados del servidor para solicitud de nombre (/nombre)")
        print("Process beacon_scan and history OK")


Process(target=get_beacons_scan).start()


@app.route('/')
def hola():
    return 'Person Name by Wisrovi'


@app.route('/history', methods=['GET'])
def history():
    data = read_file()
    return json.dumps(data, indent=4)


@app.route('/name', methods=['GET'])
def name():
    data = dict()
    try:
        with open(FILE_PERSON_SCAN) as json_file:
            data = json.load(json_file)
    except:
        pass
    return json.dumps(data, indent=4)


@app.route('/mirror', methods=['GET'])
def mirror():
    BEACON_FILE = dict()
    try:
        with open(FILE_BEACON_SCAN) as json_file:
            BEACON_FILE = json.load(json_file)
    except:
        pass
    return json.dumps(BEACON_FILE, indent=4)


@app.route('/help')
def help_service():
    OBJ = dict()

    options_config = list()
    options_config.append("look copy beacons now")
    OBJ['http://localhost:5004/mirror'] = options_config

    options_send = list()
    options_send.append("return last name received")
    OBJ['http://localhost:5004/name'] = options_send

    options_send = list()
    options_send.append("return all history beacon - names since last create service")
    OBJ['http://localhost:5004/history'] = options_send

    return json.dumps(OBJ, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
