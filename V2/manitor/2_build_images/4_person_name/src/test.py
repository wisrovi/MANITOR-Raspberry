import requests

MAC_RPI = requests.get('http://' + "192.168.1.110" + ':5003/mac', params={}, timeout=10)
MAC_RPI = MAC_RPI.text
print("\n\n La mac de la RPI es: {} \n\n".format(MAC_RPI))