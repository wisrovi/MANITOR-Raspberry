FOLDER = "resources/"

videos = dict()
videos['1'] = FOLDER + "manos/" + "1_morjarse_manos_15fps.mp4"
videos['2'] = FOLDER + "manos/" + "2_aplique_jabon_15fps.mp4"
videos['3'] = FOLDER + "manos/" + "3_palma_con_palma_15fps.mp4"
videos['4'] = FOLDER + "manos/" + "4_detras_manos_15fps.mp4"
videos['5'] = FOLDER + "manos/" + "5_entre_ dedos _15fps.mp4"
videos['6'] = FOLDER + "manos/" + "6_detras_dedos_15fps.mp4"
videos['7'] = FOLDER + "manos/" + "7_pulgares_15fps.mp4"
videos['8'] = FOLDER + "manos/" + "8_unas_15 fps.mp4"
videos['9'] = FOLDER + "manos/" + "9_munecas_15fps.mp4"
videos['10'] = FOLDER + "manos/" + "10_enjuaga_seca_15fps.mp4"

textos = dict()
textos['1'] = "Moje ambas manos con agua"
textos['2'] = "aplique abundante jabón"
textos['3'] = "frote ambas palmas vigorosamente"
textos['4'] = "frote el dorso de cada mano"
textos['5'] = "frote ambas palmas con los dedos entrelazados"
textos['6'] = "frote el dorso de los dedos con las palmas de la manos"
textos['7'] = "frote el dedo pulgar"
textos['8'] = "frote la punta de los dedos con las palmas"
textos['9'] = "frote cada muñeca con la mano opuesta"
textos['10'] = "es el momento de enjuagarse las manos"

cronometros = dict()
cronometros['2'] = FOLDER + "crono/" + "2_seg_cronometro_15fps.mp4"
cronometros['3'] = FOLDER + "crono/" + "3_seg_cronometro_15fps.mp4"
cronometros['4'] = FOLDER + "crono/" + "4_seg_cronometro_15fps.mp4"
cronometros['5'] = FOLDER + "crono/" + "5_seg_cronometro_15fps.mp4"
cronometros['6'] = FOLDER + "crono/" + "6_seg_cronometro_15fps.mp4"
cronometros['7'] = FOLDER + "crono/" + "7_seg_cronometro_15fps.mp4"
cronometros['8'] = FOLDER + "crono/" + "8_seg_cronometro_15fps.mp4"
cronometros['9'] = FOLDER + "crono/" + "9_seg_cronometro_15fps.mp4"


class Recurso:
    video = None
    texto = None
    cronometro = None
    time = 0

    def __init__(self, paso, time=2):
        self.video = videos.get(str(paso))
        self.texto = textos.get(str(paso))
        self.cronometro = cronometros[str(time)]
        self.time = time

    def json(self):
        return self.__dict__


Sincro = dict()
Sincro["1"] = Recurso(paso=1, time=8).json()
Sincro['2'] = Recurso(paso=2, time=5).json()
Sincro['3'] = Recurso(paso=3, time=8).json()
Sincro['4'] = Recurso(paso=4, time=7).json()
Sincro['5'] = Recurso(paso=5, time=9).json()
Sincro['6'] = Recurso(paso=6, time=6).json()
Sincro['7'] = Recurso(paso=7, time=5).json()
Sincro['8'] = Recurso(paso=8, time=8).json()
Sincro['9'] = Recurso(paso=9, time=9).json()
Sincro['10'] = Recurso(paso=10, time=9).json()

if __name__ == '__main__':
    tiempo_total = 0
    for key, value in Sincro.items():
        print(key, value)
        tiempo_total += value['time']
    print("Tiempo total lavado de manos:", tiempo_total, "segundos")
