videos = list()
videos.append("VIDEOS/paso1.mp4")
videos.append("VIDEOS/paso2.mp4")
videos.append("VIDEOS/paso3.mp4")
videos.append("VIDEOS/paso4.mp4")
videos.append("VIDEOS/paso5.mp4")
videos.append("VIDEOS/paso6.mp4")
videos.append("VIDEOS/paso7.mp4")
videos.append("VIDEOS/paso8.mp4")
videos.append("VIDEOS/paso9.mp4")
videos.append("VIDEOS/paso10.mp4")

cronometros = dict()
cronometros['2'] = "CRONOMETRO/CRONO2seg.mp4"
cronometros['3'] = "CRONOMETRO/CRONO3seg.mp4"
cronometros['4'] = "CRONOMETRO/CRONO4seg.mp4"
cronometros['5'] = "CRONOMETRO/CRONO5seg.mp4"
cronometros['6'] = "CRONOMETRO/CRONO6seg.mp4"
cronometros['7'] = "CRONOMETRO/CRONO7seg.mp4"
cronometros['8'] = "CRONOMETRO/CRONO8seg.mp4"
cronometros['9'] = "CRONOMETRO/CRONO9seg.mp4"

textos = list()
textos.append("Moje ambas manos con agua")
textos.append("aplique abundante jabón")
textos.append("ahora, frote ambas palmas vigorosamente")
textos.append("ahora, frote el dorso de cada mano")
textos.append("ahora, frote ambas palmas con los dedos entrelazados")
textos.append("frote el dorso de los dedos con las palmas de la manos")
textos.append("ahora frote el dedo pulgar")
textos.append("ahora frote la punta de los dedos con las palmas")
textos.append("ahora, frote cada muñeca con la mano opuesta")
textos.append("es el momento de enjuagarse las manos")

audios = list()
audios.append("VOCES/DIALOGOS/01bienvenidoAlManitor.mp3")
audios.append("VOCES/DIALOGOS/02MojeAmbasManosConAgua.mp3")
audios.append("VOCES/DIALOGOS/03apliqueAbundanteJabon.mp3")
audios.append("VOCES/DIALOGOS/04FroteAmbasPalmasVigorosamente.mp3")
audios.append("VOCES/DIALOGOS/05ahora frote el dorso de cada mano.mp3")
audios.append("VOCES/DIALOGOS/06AhoraFroteAmbasPalmasConLosDedosEntrelazados.mp3")
audios.append("VOCES/DIALOGOS/07SFroteElDorsoDeLosDedosConLasPalmasDeLasManos.mp3")
audios.append("VOCES/DIALOGOS/08AhoraFroteElDedoPulgar.mp3")
audios.append("VOCES/DIALOGOS/09AhoraFroteLaPuntaDeLosDedosConLasPalmas.mp3")
audios.append("VOCES/DIALOGOS/10FroteCadaMunecaConLaManoOpuesta.mp3")
audios.append("VOCES/DIALOGOS/11esElMomentoDeEnjuagarseLasManos.mp3")


class Recurso:
    video = None
    texto = None
    audio = None
    cronometro = None
    time = 0

    def __init__(self, vid, tex, aud, time=2):
        self.video = vid
        self.texto = tex
        self.audio = aud
        self.cronometro = cronometros[str(time)]
        self.time = time

    def json(self):
        return self.__dict__


audiovisual = list()
audiovisual.append(Recurso(vid=videos[0], tex=textos[0], aud=audios[1], time=8).json()) # 0
audiovisual.append(Recurso(vid=videos[1], tex=textos[1], aud=audios[2], time=5).json()) # 1
audiovisual.append(Recurso(vid=videos[2], tex=textos[2], aud=audios[3], time=8).json()) # 2
audiovisual.append(Recurso(vid=videos[6], tex=textos[3], aud=audios[4], time=7).json()) # 3
audiovisual.append(Recurso(vid=videos[3], tex=textos[4], aud=audios[5], time=9).json()) # 4
audiovisual.append(Recurso(vid=videos[4], tex=textos[5], aud=audios[6], time=6).json()) # 5 # pendiente revisar, falta video dorso dedos con palmas de manos
audiovisual.append(Recurso(vid=videos[5], tex=textos[6], aud=audios[7], time=5).json()) # 6
audiovisual.append(Recurso(vid=videos[7], tex=textos[7], aud=audios[8], time=8).json()) # 7
audiovisual.append(Recurso(vid=videos[8], tex=textos[8], aud=audios[9], time=9).json()) # 8
audiovisual.append(Recurso(vid=videos[9], tex=textos[9], aud=audios[10], time=9).json()) # 9


id = 9
for i, _ in enumerate(audiovisual):
    print(f"++++++++++++ Pose: {i+1} ++++++++++++")
    for key, value in audiovisual[i].items():
        print(f'{key}:', value)
    print()
    if i == id:
        break
