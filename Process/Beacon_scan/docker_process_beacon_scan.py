TIME_SCAN = 5
NAME_FILE_BEACON = "json_beacon_scan.json"

import json
import time








from ScanUtility import beacontools








PRINT_LOG = True
scan_beacon = beacontools(0, TIME_SCAN)


def main_beacon_scan():
    scan_beacon.start_continue_process()

    FOLDER = "/home/Beacon/"

    while True:
        BEACONS = scan_beacon.get_beacons()

        OBJ = dict()
        for key, beacon_class in BEACONS.items():
            OBJ[key] = beacon_class.getJson()
            if PRINT_LOG:
                print(beacon_class.getJson())

        if PRINT_LOG:
            print("Escaneando")

        with open(FOLDER + NAME_FILE_BEACON, 'w') as outfile:
            json.dump(OBJ, outfile)

        time.sleep(TIME_SCAN)
    scan_beacon.detener_continue_process()


if __name__ == '__main__':
    main_beacon_scan()
