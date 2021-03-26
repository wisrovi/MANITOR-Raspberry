BROKER_MQTT = "18.206.230.254"  # ip del broker
PORT_MQTT = 2883  # puerto del broker
USER = ""
PWD = ""


def Get_MAC():
    import getmac
    mac = getmac.get_mac_address()
    return mac


PROJECT = "/SPINPLM/"

TOPICS_USAR = list()
TOPICS_USAR.append(PROJECT + "restart")
TOPICS_USAR.append(PROJECT + "OTA")
TOPICS_USAR.append(PROJECT + Get_MAC() + "/restart")
TOPICS_USAR.append(PROJECT + Get_MAC() + "/OTA")

FILE_MQTT = "mqtt.json"
