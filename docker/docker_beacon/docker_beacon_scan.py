"""
    CONFIG
"""
TIME_SCAN = 5
NAME_FILE_BEACON = "json_beacon_scan.json"

"""
    Clases
"""

# https://github.com/bowdentheo/BLE-Beacon-Scanner

class Beacon_Obj(object):
    mac = str()
    rssi = int()
    uuid = str()
    tx_power = int()
    major = int()
    minor = int()
    tipo = str()
    empresa = str()

    def __init__(self, mac: str, rssi: int, uuid: str, tx: int, maj: int, min: int, tip: str, company: str):
        self.mac = mac
        self.rssi = rssi
        self.uuid = uuid
        self.tx_power = tx
        self.major = maj
        self.minor = min
        self.tipo = tip
        self.empresa = company

    def getJson(self):
        return self.__dict__


class beacontools:
    import sys
    import struct
    import bluetooth._bluetooth as bluez
    from multiprocessing import Process, Queue
    import time

    OGF_LE_CTL = 0x08
    OCF_LE_SET_SCAN_ENABLE = 0x000C

    BEACONs_SCANNED = dict()

    def __init__(self, dev_id, time_use):
        self.proc = self.Process(target=self.__continue_process)
        self.time_use = time_use
        try:
            self.sock = self.bluez.hci_open_dev(dev_id)
            print("\n *** Looking for BLE Beacons ***\n")
        except:
            self.sock = None
            print("Error accessing bluetooth")
        self.queue = self.Queue()

    def hci_enable_le_scan(self):
        if self.sock is not None:
            self.hci_toggle_le_scan(0x01)

    def hci_disable_le_scan(self):
        if self.sock is not None:
            self.hci_toggle_le_scan(0x00)

    def hci_toggle_le_scan(self, enable):
        if self.sock is not None:
            cmd_pkt = self.struct.pack("<BB", enable, 0x00)
            self.bluez.hci_send_cmd(self.sock, self.OGF_LE_CTL, self.OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

    def packetToString(self, packet):
        """
        Returns the string representation of a raw HCI packet.
        """
        if self.sys.version_info > (3, 0):
            return ''.join('%02x' % self.struct.unpack("B", bytes([x]))[0] for x in packet)
        else:
            return ''.join('%02x' % self.struct.unpack("B", x)[0] for x in packet)

    def parse_events(self, loop_count=100):
        global prefix
        if self.sock is not None:
            # old_filter = self.sock.getsockopt( self.bluez.SOL_HCI, self.bluez.HCI_FILTER, 14)
            flt = self.bluez.hci_filter_new()
            self.bluez.hci_filter_all_events(flt)
            self.bluez.hci_filter_set_ptype(flt, self.bluez.HCI_EVENT_PKT)
            self.sock.setsockopt(self.bluez.SOL_HCI, self.bluez.HCI_FILTER, flt)
            results = []
            for i in range(0, loop_count):
                packet = self.sock.recv(255)
                # ptype, event, plen = self.struct.unpack("BBB", packet[:3])
                packetOffset = 0
                dataString = self.packetToString(packet)
                """
                If the bluetooth device is an beacon then show the beacon.
                """
                # print (dataString)
                if (dataString[34:42] == '0303aafe') and (dataString[44:50] == '16AAFE'):
                    """
                    Selects parts of the bluetooth packets.
                    """
                    broadcastType = dataString[50:52]
                    if broadcastType == '00':
                        type = "Eddystone UID"
                        namespace = dataString[54:74].upper()
                        instance = dataString[74:86].upper()
                        resultsArray = [
                            {"type": type, "namespace": namespace, "instance": instance}]
                        return resultsArray

                    elif broadcastType == '10':
                        type = "Eddystone URL"
                        urlprefix = dataString[54:56]
                        if urlprefix == '00':
                            prefix = 'http://www.'
                        elif urlprefix == '01':
                            prefix = 'https://www.'
                        elif urlprefix == '02':
                            prefix = 'http://'
                        elif urlprefix == '03':
                            prefix = 'https://'
                        hexUrl = dataString[56:][:-2]
                        if self.sys.version_info[0] == 3:
                            url = prefix + bytes.fromhex(hexUrl).decode('utf-8')
                            rssi, = self.struct.unpack("b", bytes([packet[packetOffset - 1]]))
                        else:
                            url = prefix + hexUrl.decode("hex")
                            rssi, = self.struct.unpack("b", packet[packetOffset - 1])
                        resultsArray = [{"type": type, "url": url}]
                        return resultsArray

                    elif broadcastType == '20':
                        type = "Eddystone TLM"
                        resultsArray = [{"type": type}]
                        return resultsArray

                    elif broadcastType == '30':
                        type = "Eddystone EID"
                        resultsArray = [{"type": type}]
                        return resultsArray

                    elif broadcastType == '40':
                        type = "Eddystone RESERVED"
                        resultsArray = [{"type": type}]
                        return resultsArray

                if dataString[38:46] == '4c000215':
                    """
                    Selects parts of the bluetooth packets.
                    """
                    type = "iBeacon"
                    uuid = dataString[46:54] + "-" + dataString[54:58] + "-" + dataString[58:62] + "-" + dataString[
                                                                                                         62:66] + "-" + dataString[
                                                                                                                        66:78]
                    major = dataString[78:82]
                    minor = dataString[82:86]
                    majorVal = int("".join(major.split()[::-1]), 16)
                    minorVal = int("".join(minor.split()[::-1]), 16)
                    """
                    Organises Mac Address to display properly
                    """
                    scrambledAddress = dataString[14:26]
                    fixStructure = iter(
                        "".join(reversed([scrambledAddress[i:i + 2] for i in range(0, len(scrambledAddress), 2)])))
                    macAddress = ':'.join(a + b for a, b in zip(fixStructure, fixStructure))
                    if self.sys.version_info[0] == 3:
                        rssi, = self.struct.unpack("b", bytes([packet[packetOffset - 1]]))
                    else:
                        rssi, = self.struct.unpack("b", packet[packetOffset - 1])

                    resultsArray = [{"type": type, "uuid": uuid, "major": majorVal, "minor": minorVal, "rssi": rssi,
                                     "macAddress": macAddress}]

                    for item in resultsArray:
                        beacon = Beacon_Obj(item['macAddress'], item['rssi'], item['uuid'], 0, item['major'],
                                            item['minor'], item['type'], item['uuid'][0:8])
                        self.BEACONs_SCANNED[beacon.uuid] = beacon
                    return resultsArray

            return results
        return []

    def __continue_process(self):
        self.time_sleep = self.time.time()
        while True:
            self.parse_events(10)
            self.time.sleep(0.25)
            if (int(abs(self.time_sleep - self.time.time()) * 100) / 100) >= self.time_use:
                self.queue.put(self.BEACONs_SCANNED)
                self.BEACONs_SCANNED = dict()
                self.time_sleep = self.time.time()

    def start_continue_process(self):
        self.hci_enable_le_scan()
        self.proc.start()

    def detener_continue_process(self):
        self.proc.terminate()
        self.proc.join()

    def get_beacons(self):
        return self.queue.get()







"""
    Proceso
"""

class Process_beacon_scan(object):
    def __init__(self):
        self.scan_beacon = beacontools(0, TIME_SCAN)

    def main_beacon_scan(self):
        import json
        import time
        self.scan_beacon.start_continue_process()

        FOLDER = "/home/Beacon/"

        while True:
            BEACONS = self.scan_beacon.get_beacons()

            OBJ = dict()
            for key, beacon_class in BEACONS.items():
                OBJ[key] = beacon_class.getJson()
                print(beacon_class.getJson())

            print("Escaneando")

            with open(FOLDER + NAME_FILE_BEACON, 'w') as outfile:
                json.dump(OBJ, outfile)

            time.sleep(TIME_SCAN)
        scan_beacon.detener_continue_process()


"""
    Ejecutor unico para que solo se ejecute en este archivo
"""

if __name__ == '__main__':
    Process_beacon_scan().main_beacon_scan()