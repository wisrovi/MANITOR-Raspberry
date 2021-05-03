import requests
import getmac
SERVER = "localhost"
NAME_SIMULING = "WilliamRodriguez"

def get_mac():
    mac = getmac.get_mac_address()
    return mac


def get_topic():
    PROJECT = "SPINPLM"
    topic = "/" + PROJECT + "/manitor/" + get_mac() + "/" + "nombre"
    return topic


PARAMS = dict()
url = 'http://' + SERVER + ':5003/send?msg=' + NAME_SIMULING + '&topic=' + get_topic()
r = requests.get(url, params=PARAMS, timeout=10)
print(r.json())