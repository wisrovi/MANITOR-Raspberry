from Process.Videos_Sound_Avatar_Screen.Config_Videos_Sound_Screen.Instrucciones_Videos import \
    LISTADO_VIDEOS_INSTRUCCIONES
from Util.Util import Util

REINICIAR_VIDEO = -1
VIDEOS = [ i for i in range(len(LISTADO_VIDEOS_INSTRUCCIONES)) ]
print(VIDEOS)

Util().save_video_show(-1)



