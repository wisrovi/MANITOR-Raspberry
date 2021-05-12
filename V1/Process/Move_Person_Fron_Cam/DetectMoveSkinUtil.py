


class Deteccion_movimiento:
    import cv2
    import numpy as np
    import json
    import os
    from time import strftime
    from Process.Move_Person_Fron_Cam.config_movimiento_frente_camara import STATUS_MOVIMIENTO, valor_cambio, \
        TIEMPO_POR_INSTRUCCION, constante_cambio_area
    from Process.Move_Person_Fron_Cam.config_movimiento_frente_camara import FILE_CONFIG_MOVE_DETECT

    chrono_siguiente_instruccion = None
    chrono_tiempo_alerta = None

    PROCESS_DETECT_MOVE = False
    primer_movimiento_secuencia = False
    status = STATUS_MOVIMIENTO[1]
    contador_cambio_estado = 0
    dm = None

    cap = None

    last_areas = list()

    def __init__(self, cam, clase):
        self.elegir_camara(cam)
        self.instanciar_clase(clase)
        self.tiempo = self.TIEMPO_POR_INSTRUCCION

        OBJ = dict()
        with open(self.os.path.dirname(self.os.path.realpath(__file__)) + "/" + self.FILE_CONFIG_MOVE_DETECT) as json_file:
            OBJ = self.json.load(json_file)
            # print(OBJ)

        colores = dict()
        colores['piel'] = (self.CreateColor(OBJ["H_min"], OBJ["S_min"], OBJ["V_min"]), self.CreateColor(OBJ["H_max"], OBJ["S_max"], OBJ["V_max"]))
        # colores['verde'] = (self.CreateColor(34, 177, 76), self.CreateColor(255, 255, 255))
        self.franja_colores = {
            "min": colores["piel"][0],
            "max": colores["piel"][1]
        }

    def LeerFotograma(self, cap):
        _, frame = cap.read()
        # cv2.imshow("Original Image", frame)
        return frame

    def CreateColor(self, h=0, s=0, v=0):
        # HSV -> H[0 a 179], S[0 a 255], V[0 a 255]
        return self.np.array([h, s, v])

    def CrearMascara(self, frame):
        masking, punto_elegido = None, None
        if frame is not None:
            # convierto la imagen a HSV para quitar capas y mejorar el procesamiento
            hsv_img = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2HSV)

            # Creo una mascara, donde pinto en blanco el color a buscar (color piel) y en negro lo que no cumpla dentro del color de interes
            masking = self.cv2.inRange(hsv_img, self.franja_colores["min"], self.franja_colores["max"])

            # eliminamos el ruido
            if False:
                kernel = np.ones((10, 10), np.uint8)
                masking = cv2.morphologyEx(masking, cv2.MORPH_OPEN, kernel)
                masking = cv2.morphologyEx(masking, cv2.MORPH_CLOSE, kernel)

            # Detectamos contornos, nos quedamos con el mayor y calculamos su centro
            punto_elegido = 0
            if False:
                contours, hierarchy = cv2.findContours(masking, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                mayor_contorno = max(contours, key=cv2.contourArea)
                momentos = cv2.moments(mayor_contorno)
                cx = float(momentos['m10'] / momentos['m00'])
                cy = float(momentos['m01'] / momentos['m00'])
                punto_elegido = np.array([[[cx, cy]]], np.float32)

            # cv2.imshow("Deteccion Color", masking)
        return masking, punto_elegido

    def QuitarPartesNoMarcadasEnMascara(self, frame, masking):
        # Creo una nueva imagen tomando la imagen original y dejando solo las partes blancas de la mascara
        new_img = self.cv2.bitwise_and(frame, frame, mask=masking)
        return new_img

    def FrameSinRuido(self, cap):
        # ********* Paso 1: Leo el fotograma de la camara
        frame = self.LeerFotograma(cap)

        # ********* Paso 2: Detecto el color piel y el resto de colores los elimino dejando una mascara con blanco (color de interes) y negro (otros colores)
        masking, punto_elegido = self.CrearMascara(frame)

        # ********* Paso 3: tomo la imagen original y le aplico la mascara, para tener la imagen original sin los colores NO deseados
        new_img = self.QuitarPartesNoMarcadasEnMascara(frame, masking)
        return new_img, punto_elegido, frame, masking

    def hallar_contornos_areas(self, frame, masking):
        thresh = self.cv2.threshold(masking, 25, 255, self.cv2.THRESH_BINARY)[
            1]  # (masking,127,255,   0) # Aplicamos un umbral para quitar ruido
        thresh = self.cv2.dilate(thresh, None, iterations=2)  # Dilatamos el umbral para tapar agujeros

        contornos = self.cv2.findContours(thresh, self.cv2.RETR_TREE, self.cv2.CHAIN_APPROX_SIMPLE)[
            0]  # CHAIN_APPROX_SIMPLE: deja solo los contornos externos obviando los internos (ahorrar memoria y aumentar velocidad computo)

        cajas = list()
        areas = list()
        contornos_finales = list()
        for c in contornos:  # Recorremos todos los contornos encontrados
            if self.cv2.contourArea(c) < self.constante_cambio_area:  # Eliminamos los contornos mas pequenos
                continue
            (x, y, w, h) = self.cv2.boundingRect(
                c)  # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
            self.cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cajas.append((x, y, x + w, y + h))
            contornos_finales.append(c)

            area = w * h
            areas.append(area)

        self.cv2.drawContours(frame, contornos_finales, -1, (255, 0, 0), 3)

        # Determinar movimiento de acuerdo a el cambio de areas (superior a una constante definida) en objeto(s) en la escena
        hay_movimiento_segun_cambio_areas = False
        if len(self.last_areas) == len(
                areas):  # if exist(True) in list(  if abs(valor)>constante*1.5 => valor = resta(last_areas, areas)  )
            hay_movimiento_segun_cambio_areas = True if True in [True if i > self.constante_cambio_area * 1.5 else False
                                                                 for i in
                                                                 [abs(i) for i in [e1 - e2 for e1, e2 in
                                                                                   zip(self.last_areas,
                                                                                       areas)]]] else False
        else:
            hay_movimiento_segun_cambio_areas = True
            pass
        self.last_areas = areas

        return cajas, areas, hay_movimiento_segun_cambio_areas

    def currentTime(self):  # Obtain current time in seconds
        now = self.strftime("%H,%M,%S")
        (h, m, s) = now.split(',')
        currentTime = int(h) * 3600 + int(m) * 60 + int(s)
        return currentTime

    def instanciar_clase(self, f):
        self.dm = f()
        self.chrono_siguiente_instruccion = self.currentTime()
        self.chrono_tiempo_alerta = self.currentTime()

    def iniciar_proceso_deteccion_movimiento(self):
        self.PROCESS_DETECT_MOVE = True
        self.primer_movimiento_secuencia = False
        self.status = self.STATUS_MOVIMIENTO[0]
        self.contador_cambio_estado = 0

        self.dm.iniciar_proceso()

    def terminar_proceso_deteccion_movimiento(self):
        self.PROCESS_DETECT_MOVE = False
        self.primer_movimiento_secuencia = False
        self.status = self.STATUS_MOVIMIENTO[1]
        self.contador_cambio_estado = 0

    def hay_movimiento(self):
        return self.PROCESS_DETECT_MOVE

    def activar_siguiente_video(self):
        self.dm.mostrar_siguiente_video()

    def elegir_camara(self, cam):
        self.cap = self.cv2.VideoCapture(cam)

    def cerrar_camara(self):
        self.cap.release()

    def set_time(self, time_new):
        self.tiempo = time_new

    def get_frame(self):
        frame, _, _, masking = self.FrameSinRuido(self.cap)
        _, _, hay_movimiento_segun_cambio_areas = self.hallar_contornos_areas(frame, masking)

        if self.PROCESS_DETECT_MOVE:
            if hay_movimiento_segun_cambio_areas:
                self.cv2.circle(frame, (50, 50), 20, (0, 0, 255), -1)
            else:
                self.cv2.circle(frame, (50, 50), 20, (255, 0, 255), -1)

            if hay_movimiento_segun_cambio_areas:
                if not self.primer_movimiento_secuencia:
                    self.primer_movimiento_secuencia = True
                    self.chrono_siguiente_instruccion = self.currentTime()
                    self.dm.primer_movimiento_detectado()

                if self.status == self.STATUS_MOVIMIENTO[0]:
                    self.contador_cambio_estado = 0
                else:
                    # si antes no habia movimiento y ahora si lo hay se valida que no se falso positivo al monitorear que el movimiento sea continuo frente a la camara
                    self.contador_cambio_estado += 1
                    if self.contador_cambio_estado > self.valor_cambio / 2:
                        self.status = self.STATUS_MOVIMIENTO[0]
                        self.chrono_siguiente_instruccion = self.currentTime()

                if self.status == self.STATUS_MOVIMIENTO[0]:
                    if abs(self.chrono_siguiente_instruccion - self.currentTime()) >= self.tiempo:
                        self.chrono_siguiente_instruccion = self.currentTime()
                        self.activar_siguiente_video()
            else:
                if self.primer_movimiento_secuencia:
                    if self.status == self.STATUS_MOVIMIENTO[0]:
                        self.contador_cambio_estado += 1
                        if self.contador_cambio_estado == int(self.valor_cambio / 4):
                            self.dm.primer_preaviso_no_movimiento()

                        if self.contador_cambio_estado == int(self.valor_cambio / 3):
                            self.dm.segundo_preaviso_no_movimiento()

                        if self.contador_cambio_estado == int(self.valor_cambio / 2):
                            self.dm.tercer_preaviso_no_movimiento()
                            self.chrono_siguiente_instruccion = self.currentTime()

                        if self.contador_cambio_estado >= int(self.valor_cambio / 1):
                            self.dm.proceso_interrumpido_por_superar_tres_advertencias()
                            self.terminar_proceso_deteccion_movimiento()
                    else:
                        self.contador_cambio_estado = 0

        return frame

    def reiniciar_tiempo_instruccion(self):
        self.chrono_siguiente_instruccion = self.currentTime()


if __name__ == "__main__":
    pass
