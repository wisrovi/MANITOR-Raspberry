import requests


SERVER = "localhost"
PARAMS = dict()
r = requests.get('http://' + SERVER + ':5001/beacons', params=PARAMS, timeout=10)
BEACON_SCAN_FILE = r.json()

print(BEACON_SCAN_FILE)