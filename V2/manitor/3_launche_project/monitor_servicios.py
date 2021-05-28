import requests
import json
import time


def get(url):
    DATA = requests.get(url, params={}, timeout=10)
    status_code = DATA.status_code
    text = DATA.text
    return status_code, text


def test_5006():
    url = 'http://' + ip + ':5006/move'
    rta = get(url)
    msg = rta[1]

    OBJ = dict()
    OBJ["online"] = "OK" if responses["5006"][0] == 200 else "BAD"

    if len(msg) > 6:
        msg = json.loads(msg)
        move = msg['move']
        acc = msg['acc']

        OBJ["move"] = move
        OBJ["acc"] = acc

    microservicios['5006'] = OBJ


def test_5004():
    url = 'http://' + ip + ':5004/name'
    rta = get(url)
    msg = rta[1]

    OBJ = dict()
    OBJ["online"] = "OK" if responses["5004"][0] == 200 else "BAD"

    if len(msg) > 6:
        msg = json.loads(msg)
        data = [key for key in msg['data']][0]
        name = msg['name']

        OBJ["uuid"] = data
        OBJ["name"] = name

    microservicios['5004'] = OBJ


def test_5003():
    url = 'http://' + ip + ':5003/topics'
    rta = get(url)
    msg = rta[1]

    OBJ = dict()
    OBJ["online"] = "OK" if responses["5003"][0] == 200 else "BAD"

    if len(msg) > 6:
        msg = json.loads(msg)
        conected = True if len(msg) > 0 else False
        OBJ["conected_mqtt"] = conected

    microservicios['5003'] = OBJ


def test_others():
    microservicios['5001'] = {"online": "OK" if responses["5001"][0] == 200 else "BAD"}
    microservicios['5002'] = {"online": "OK" if responses["5002"][0] == 200 else "BAD"}
    microservicios['5005'] = {"online": "OK" if responses["5005"][0] == 200 else "BAD"}
    microservicios['5007'] = {"online": "OK" if responses["5007"][0] == 200 else "BAD"}
    microservicios['5008'] = {"online": "OK" if responses["5008"][0] == 200 else "BAD"}


ip = "192.168.1.112"
while True:
    responses = dict()
    for i in range(1, 9, 1):
        try:
            url = 'http://' + ip + f':500{str(i)}'
            responses[f'500{str(i)}'] = get(url)
        except:
            pass

    microservicios = dict()

    test_5003()
    test_5004()
    test_5006()
    test_others()

    print()
    print()


    microservicios = sorted(microservicios.items())
    for key, value in microservicios:
        print(key, value)

    time.sleep(2)
