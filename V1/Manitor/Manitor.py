
class MANITOR(object):
    from Process.Util.Util import Util
    from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import \
        LISTADO_VIDEOS_INSTRUCCIONES

    def __init__(self):
        self.util = self.Util()

    def reportar_correcto_lavado_manos(self, uuid):
        self.util.enviar_mqtt(uuid=uuid)

    def read_beacons(self):
        return self.util.read_data_scan_beacon()

    def video_instruccion_mostrar_video(self, id_video: int):
        self.util.save_video_show(id_video)

    def video_instruccion_reiniciar(self):
        self.util.save_video_show(-1)

    def get_data_video(self, id):
        if id == len(self.LISTADO_VIDEOS_INSTRUCCIONES):
            id -= 1
        video = self.LISTADO_VIDEOS_INSTRUCCIONES[id]
        return video['id'], video['time'], video['path'].split('.')[0]
