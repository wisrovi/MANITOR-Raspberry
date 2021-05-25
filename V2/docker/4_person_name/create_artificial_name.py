import requests

SERVER = "192.168.1.106"
NAME_SIMULING = "WilliamRodriguez"


def get_mac():
    mac = "dc:a6:32:34:07:0f"
    return mac


def get_topic():
    PROJECT = "SPINPLM"
    topic = "/" + PROJECT + "/manitor/" + get_mac() + "/" + "nombre"
    return topic


PARAMS = dict()
url = 'http://' + SERVER + ':5003/send?msg=' + NAME_SIMULING + '&topic=' + get_topic()

print(url)

r = requests.get(url, params=PARAMS, timeout=10)
print(r.json())
