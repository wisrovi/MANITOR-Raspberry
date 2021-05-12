NAME_FILE_SOUND = "json_sound.json"
TIME_SCAN_FILE_SOUND = 1


class File_New_Sound(object):
    numero_audio = int()
    visto = bool()

    def __init__(self, number, show):
        self.numero_audio = number
        self.visto = show

    def getJson(self):
        return self.__dict__