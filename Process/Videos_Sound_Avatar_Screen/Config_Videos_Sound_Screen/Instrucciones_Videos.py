def CreateInstruccion(path_video, id, name="paso", time=0):
    inst = dict()
    inst['path'] = path_video
    inst['name'] = name + " " + str(id)
    inst['id'] = id
    inst['time'] = time
    return inst


LISTADO_VIDEOS_INSTRUCCIONES = list()
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=0, path_video='0_bienvenida.mp4', time=10))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=1, path_video='1_mojarse_manos.mp4', time=10))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=2, path_video='2_aplique_jabon.mp4', time=11))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=3, path_video='3_palma_con_palma.mp4', time=8))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=4, path_video='5_detras_manos.mp4', time=13))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=5, path_video='4_entre_dedos.mp4', time=9))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=6, path_video='7_detras_dedos.mp4', time=12))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=7, path_video='6_pulgares.mp4', time=14))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=8, path_video='8_unas.mp4', time=15))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=9, path_video='9_munecas.mp4', time=7))
LISTADO_VIDEOS_INSTRUCCIONES.append(CreateInstruccion(id=10, path_video='10_enjuagarSecar.mp4', time=16))

CHECK_NEW_VIDEO = 3


class File_New_Video(object):
    numero_paso = int()
    visto = bool()

    def __init__(self, number, show):
        self.numero_paso = number
        self.visto = show

    def getJson(self):
        return self.__dict__
