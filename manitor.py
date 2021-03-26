from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import \
    LISTADO_VIDEOS_INSTRUCCIONES
from Process.Util import Util

util = Util()
util.enviar_mqtt(uuid="1234567890abcdefghijklmnoprstuvwxyz")


print( util.read_data_scan_beacon() )


REINICIAR_VIDEO = -1
VIDEOS = [ i for i in range(len(LISTADO_VIDEOS_INSTRUCCIONES)) ]
VIDEOS.insert(0, REINICIAR_VIDEO)

Util().save_video_show(VIDEOS[1])