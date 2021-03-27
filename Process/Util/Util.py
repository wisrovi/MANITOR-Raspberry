class Util(object):
    import json
    import os
    from Process.Mqtt.config_mqtt import FILE_MQTT
    from Process.Beacon_scan.config_beacon import NAME_FILE_BEACON
    from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Constantes import FILE_VIDEO_CONTROL
    from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import File_New_Video

    def __init__(self):
        self.BASE_DIR = self.os.path.dirname(self.os.path.realpath(__file__))
        self.BASE_DIR_ROOT = "/".join([e for e in self.BASE_DIR.split("/")][:-1]) + "/"

    def enviar_mqtt(self, uuid):
        OBJ = dict()
        OBJ['uuid'] = uuid
        with open(self.BASE_DIR_ROOT + self.FILE_MQTT, 'w') as outfile:
            self.json.dump(OBJ, outfile)

    def read_data_scan_beacon(self):
        data = dict()
        if self.__exist_file(self.BASE_DIR_ROOT + self.NAME_FILE_BEACON):
            with open(self.BASE_DIR_ROOT + self.NAME_FILE_BEACON) as json_file:
                data = self.json.load(json_file)
        return data

    def read_video_show(self):
        data = dict()
        FILE = self.BASE_DIR_ROOT + self.FILE_VIDEO_CONTROL
        if self.__exist_file(FILE):
            with open(FILE) as json_file:
                data = self.json.load(json_file)
        else:
            pass
            # print("No existe el archivo ", self.os.getcwd(), FILE)
        return data

    def save_video_show(self, numero_video: int, visto=False):
        OBJ = self.File_New_Video(numero_video, visto).getJson()
        with open(self.BASE_DIR_ROOT + self.FILE_VIDEO_CONTROL, 'w') as outfile:
            self.json.dump(OBJ, outfile)

    def __exist_file(self, file):
        if self.os.path.isfile(file):
            return True
        else:
            return False
