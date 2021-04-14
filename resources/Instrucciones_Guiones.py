PATH_VIDEOS = "resources/"


def CreateGuion(id, text):
    guion = dict()
    guion['id'] = id
    guion['text'] = text
    return guion


GUIONES = list()
GUIONES.append(CreateGuion(id=0,
                           text="Bienvenido al sistema integrado de lavado de manos. A continuación daré unas instrucciones las cuales debe seguir para un correcto lavado de manos."))
GUIONES.append(CreateGuion(id=1, text="Primero, moje ambas manos con suficiente agua. "))
GUIONES.append(CreateGuion(id=2, text="Segundo, aplique suficiente jabón sobre la superficie de la palma de la mano."))
GUIONES.append(CreateGuion(id=3, text="Tercero, frote ambas palmas de las manos."))
GUIONES.append(CreateGuion(id=4,
                           text="Cuarto, frote el dorso de cada mano con la palma de la otra mano, teniendo los dedos entrelazados."))
GUIONES.append(CreateGuion(id=5, text="Quinto, frote ambas palmas de las manos con los dedos entrelazados."))
GUIONES.append(CreateGuion(id=6,
                           text="Sexto, frote con el dorso de los dedos las palmas de la manos, teniendo los dedos entrelazados."))
GUIONES.append(CreateGuion(id=7, text="Séptimo, presione y rote cada dedo pulgar con la mano opuesta."))
GUIONES.append(CreateGuion(id=8,
                           text="Octavo, frote las puntas de los dedos con la palma opuesta teniendo un movimiento circular"))
GUIONES.append(CreateGuion(id=9, text="Noveno, frote cada muñeca con la mano opuesta."))
GUIONES.append(CreateGuion(id=10, text="Decimo, enjuague sus manos con suficiente agua."))
