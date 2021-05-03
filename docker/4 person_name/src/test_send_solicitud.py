import requests
import time
import getmac
SERVER = "localhost"


def get_mac():
    mac = getmac.get_mac_address()
    return mac


def get_topic(uuid):
    PROJECT = "SPINPLM"
    topic = "/" + PROJECT + "/manitor/" + get_mac() + "/" + uuid + "/solicitud"
    return topic


failed = False

PARAMS = dict()
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

    BEACON_SCAN = BEACON_SCAN_FILE
    MORE_NEAR = dict()
    for k, v in more_near_sorted.items():
        MORE_NEAR[k] = BEACON_SCAN_FILE[k]
        break

    OBJ = dict()
    OBJ['all'] = BEACON_SCAN
    OBJ['near'] = MORE_NEAR

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
        print(data_response, data_response['data'])
