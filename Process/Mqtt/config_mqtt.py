
BROKER_MQTT_FCV = "172.30.19.92"  # ip del broker
PORT_MQTT_FCV = 1883  # puerto del broker
USER_FCV = ""
PWD_FCV = ""



BROKER_MQTT = "192.168.1.109"  # ip del broker
PORT_MQTT = 1884  # puerto del broker
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

FILE_MQTT = "json_mqtt.json"
