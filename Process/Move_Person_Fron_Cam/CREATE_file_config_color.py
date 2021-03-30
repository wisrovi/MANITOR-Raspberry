
class Configuracion_filtro_camara(object):
    import cv2
    import numpy as np

    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    ventana_config_crada = False
    primera_captura_config = False

    def __init__(self, fullscreen=False):
        self.fullscreen = fullscreen

    def abrir_camara(self):
        self.cap = self.cv2.VideoCapture(0)

    @staticmethod
    def __nothing(x):
        pass

    def Crear_ventana_config(self, aplicar_filtros):
        if aplicar_filtros:
            if self.fullscreen:
                self.cv2.namedWindow("config", self.cv2.WND_PROP_FULLSCREEN)
                self.cv2.setWindowProperty("config", self.cv2.WND_PROP_FULLSCREEN, self.cv2.WINDOW_FULLSCREEN)
            else:
                self.cv2.namedWindow("config")

            # create trackbars for color change
            self.cv2.createTrackbar('HMin', 'config', 0, 179, self.__nothing)  # Hue is from 0-179 for Opencv
            self.cv2.createTrackbar('SMin', 'config', 0, 255, self.__nothing)
            self.cv2.createTrackbar('VMin', 'config', 0, 255, self.__nothing)

            self.cv2.createTrackbar('HMax', 'config', 0, 179, self.__nothing)
            self.cv2.createTrackbar('SMax', 'config', 0, 255, self.__nothing)
            self.cv2.createTrackbar('VMax', 'config', 0, 255, self.__nothing)

            if not self.primera_captura_config:
                # Set default value for MAX HSV trackbars.
                self.cv2.setTrackbarPos('HMin', 'config', 0)
                self.cv2.setTrackbarPos('SMin', 'config', 48)
                self.cv2.setTrackbarPos('VMin', 'config', 40)

                self.cv2.setTrackbarPos('HMax', 'config', 60)
                self.cv2.setTrackbarPos('SMax', 'config', 255)
                self.cv2.setTrackbarPos('VMax', 'config', 255)
            else:
                # Set default value for MAX HSV trackbars.
                self.cv2.setTrackbarPos('HMin', 'config', self.phMin)
                self.cv2.setTrackbarPos('SMin', 'config', self.psMin)
                self.cv2.setTrackbarPos('VMin', 'config', self.pvMin)

                self.cv2.setTrackbarPos('HMax', 'config', self.phMax)
                self.cv2.setTrackbarPos('SMax', 'config', self.psMax)
                self.cv2.setTrackbarPos('VMax', 'config', self.pvMax)

            self.ventana_config_crada = True
        else:
            if self.fullscreen:
                self.cv2.namedWindow("image", self.cv2.WND_PROP_FULLSCREEN)
                self.cv2.setWindowProperty("image", self.cv2.WND_PROP_FULLSCREEN, self.cv2.WINDOW_FULLSCREEN)
            else:
                self.cv2.namedWindow("image")

    def read_frame(self, mostrar_barras=False, aplicar_filtros=False):
        self.aplicar_filtros = aplicar_filtros

        if not self.ventana_config_crada and mostrar_barras:
            self.Crear_ventana_config(aplicar_filtros)

        ret, img = self.cap.read()

        if mostrar_barras:
            self.hMin = self.cv2.getTrackbarPos('HMin', 'config')
            self.sMin = self.cv2.getTrackbarPos('SMin', 'config')
            self.vMin = self.cv2.getTrackbarPos('VMin', 'config')

            self.hMax = self.cv2.getTrackbarPos('HMax', 'config')
            self.sMax = self.cv2.getTrackbarPos('SMax', 'config')
            self.vMax = self.cv2.getTrackbarPos('VMax', 'config')

            if (self.phMin != self.hMin) | (self.psMin != self.sMin) | (self.pvMin != self.vMin) | (
                    self.phMax != self.hMax) | (self.psMax != self.sMax) | (
                    self.pvMax != self.vMax):
                print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
                    self.hMin, self.sMin, self.vMin, self.hMax, self.sMax, self.vMax))
                self.phMin = self.hMin
                self.psMin = self.sMin
                self.pvMin = self.vMin
                self.phMax = self.hMax
                self.psMax = self.sMax
                self.pvMax = self.vMax
                self.primera_captura_config = True

        if aplicar_filtros:
            # Set minimum and max HSV values to display
            lower = self.np.array([self.phMin, self.psMin, self.pvMin])
            upper = self.np.array([self.phMax, self.psMax, self.pvMax])

            hsv = self.cv2.cvtColor(img, self.cv2.COLOR_BGR2HSV)
            mask = self.cv2.inRange(hsv, lower, upper)
            output = self.cv2.bitwise_and(img, img, mask=mask)

            return output

        return img

    def mostrar_frame(self, frame, aplicar_filtros=None):
        if aplicar_filtros is not None:
            self.aplicar_filtros = aplicar_filtros

        if self.aplicar_filtros:
            self.cv2.imshow('config', frame)
        else:
            self.cv2.imshow('image', frame)

    COLORES = {
        "BLACK": (0, 0, 0),
        "BLUE": (255, 0, 0),
        "WHITE": (255, 255, 255)
    }

    def poner_texto(self, imagen, texto, color_texto, tecla_salir=None, texto2=None):
        self.cv2.putText(imagen, text=texto, org=(50, 50),
                         fontFace=self.cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=self.COLORES[color_texto],
                         thickness=2, lineType=self.cv2.LINE_AA)

        if tecla_salir is not None:
            if texto2 is None:
                texto_poner = "Oprima '{}' para continuar".format(tecla_salir)
            else:
                texto_poner = texto2
            self.cv2.putText(imagen, text=texto_poner, org=(50, imagen.shape[0 ] -50 ),
                             fontFace=self.cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=self.COLORES[color_texto],
                             thickness=2, lineType=self.cv2.LINE_AA)
        return imagen

    def capturar_tecla_oprimida(self):
        self.k = self.cv2.waitKey(30) & 0xff

    def buscar_tecla_salir(self, id_tecla=27):
        if self.k == id_tecla:
            return True
        return False

    def cerrar_camara(self):
        self.cap.release()
        self.cv2.destroyAllWindows()

    def destruir_ventana_simple(self):
        try:
            self.cv2.destroyWindow("image")
        except:
            pass

    def destruir_ventana_config(self):
        self.cv2.destroyWindow("config")
        self.ventana_config_crada = False

    def get_config(self):
        OBJ = dict()
        OBJ["H_min"] = self.phMin
        OBJ["S_min"] = self.psMin
        OBJ["V_min"] = self.pvMin

        OBJ["H_max"] = self.phMax
        OBJ["S_max"] = self.psMax
        OBJ["V_max"] = self.pvMax

        return OBJ


import json
from config_movimiento_frente_camara import FILE_CONFIG_MOVE_DETECT


tecla = {
    "ESC": 27,
    "q": ord("q"),
    "p": ord("p"),
    "g": ord("g"),
    "v": ord("v")
}

config_cam = Configuracion_filtro_camara(True)
config_cam.abrir_camara()

while True:
    img = config_cam.read_frame(False)
    if img is None:
        continue

    img = config_cam.poner_texto(img, "Posicione la camara", "WHITE", "q")

    config_cam.mostrar_frame(img)

    config_cam.capturar_tecla_oprimida()
    if config_cam.buscar_tecla_salir(tecla["q"]):
        break

config_cam.destruir_ventana_simple()

mostrar_barras_config = True
while True:
    img = config_cam.read_frame(mostrar_barras=mostrar_barras_config, aplicar_filtros=True)
    if img is None:
        continue

    if mostrar_barras_config:
        img = config_cam.poner_texto(img, "Presione 'p' para ver y probar", "WHITE", "", "la configuracion")
    else:
        img = config_cam.poner_texto(img, "Presione 'g' para guardar", "WHITE", "", "Presione 'v' para volver")

    config_cam.mostrar_frame(img, mostrar_barras_config)

    config_cam.capturar_tecla_oprimida()
    if config_cam.buscar_tecla_salir(tecla["p"]) or config_cam.buscar_tecla_salir(tecla["v"]):
        mostrar_barras_config = not mostrar_barras_config
        if mostrar_barras_config:
            config_cam.destruir_ventana_simple()
        else:
            config_cam.destruir_ventana_config()

    if config_cam.buscar_tecla_salir(tecla["g"]):
        print("Guardando config")
        OBJ = config_cam.get_config()
        with open(FILE_CONFIG_MOVE_DETECT, 'w') as outfile:
            json.dump(OBJ, outfile)
        break

    # if config_cam.buscar_tecla_salir(tecla["ESC"]):
    #     break

config_cam.cerrar_camara()
