PATH_VIDEOS = "resources/"


def CreateGuion(id, text):
    guion = dict()
    guion['id'] = id
    guion['text'] = text
    return guion


GUIONES = list()
GUIONES.append(CreateGuion(id=0, text="Bienvenido al Manitor, por favor siga las instrucciones"))
GUIONES.append(CreateGuion(id=1, text="moje ambas manos con agua"))
GUIONES.append(CreateGuion(id=2, text="aplique abundante jabón"))
GUIONES.append(CreateGuion(id=3, text="ahora, frote ambas palmas vigorosamente"))
GUIONES.append(CreateGuion(id=4, text="ahora, frote el dorso de cada mano"))
GUIONES.append(CreateGuion(id=5, text="ahora, frote ambas palmas con los dedos entrelazados."))
GUIONES.append(CreateGuion(id=6, text="Sexto, frote el dorso de los dedos con las palmas de la manos"))
GUIONES.append(CreateGuion(id=7, text="ahora forte el dedo pulgar"))
GUIONES.append(CreateGuion(id=8, text="ahora frote la punta de los dedos con las palmas"))
GUIONES.append(CreateGuion(id=9, text="ahora, frote cada muñeca con la mano opuesta."))
GUIONES.append(CreateGuion(id=10, text="es el momento de enjuagarse las manos"))

GUIONES.append(CreateGuion(id=11, text="Sistema iniciado"))
GUIONES.append(CreateGuion(id=12, text="Por favor mueva las manos"))
GUIONES.append(CreateGuion(id=13, text="Por favor repita el paso actual"))
