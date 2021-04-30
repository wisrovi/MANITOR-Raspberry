import cv2


class Lienzo(object):
    PORCENTAJE_SUPERIOR = 0.9
    PORCENTAJE_LATERAL = 0.94

    import numpy as np
    import cv2

    __MARGEN_SUPERIOR = 0
    __MARGEN_LATERAL = 0

    PORCENTAJE_MARGEN_INSTRUCCION = 0.8
    PORCENTAJE_MARGEN_CRONOMETRO = 0.95

    def __init__(self, LIENZO_MOSTRAR):  # LIENZO_MOSTRAR_VIDEOS => pixeles (alto, largo)
        self.LIENZO_MOSTRAR_VIDEOS = LIENZO_MOSTRAR
        self.black_screen = self.__crear_lienzo()

    def create_board(self):
        self.__config_margen()

        demo_title_board = self.__default_board_title()
        demo_name_board = self.__default_board_name()
        demo_instruction_board = self.__default_board_instruction()
        demo_cronometro_board = self.__default_board_cronometro()

        self.poner_titulo(demo_title_board)
        self.poner_nombre(demo_name_board)
        self.poner_instruccion(demo_instruction_board)
        self.poner_cronometro(demo_cronometro_board)

    def get_board(self):
        return self.black_screen

    """
        config
    """

    def __config_margen(self):
        self.__MARGEN_SUPERIOR = (self.LIENZO_MOSTRAR_VIDEOS[0] - (
                self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR)) / 2
        self.__MARGEN_LATERAL = (self.LIENZO_MOSTRAR_VIDEOS[1] - (
                self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL)) / 2

    def __crear_lienzo(self):
        black_screen = self.np.zeros([self.LIENZO_MOSTRAR_VIDEOS[0], self.LIENZO_MOSTRAR_VIDEOS[1], 3],
                                     dtype=self.np.uint8)
        return black_screen.copy()

    """
        crear lienzos por defecto
    """

    def __put_color_purple(self, frame):
        frame[:, :, 0] = self.np.ones(list(frame.shape)[:2]) * 125
        frame[:, :, 1] = self.np.ones(list(frame.shape)[:2]) * 0
        frame[:, :, 2] = self.np.ones(list(frame.shape)[:2]) * 125
        return frame

    def __put_color_red(self, frame):
        frame[:, :, 0] = self.np.ones(list(frame.shape)[:2]) * 0
        frame[:, :, 1] = self.np.ones(list(frame.shape)[:2]) * 0
        frame[:, :, 2] = self.np.ones(list(frame.shape)[:2]) * 255
        return frame

    def __put_color_blue(self, frame):
        frame[:, :, 0] = self.np.ones(list(frame.shape)[:2]) * 255
        frame[:, :, 1] = self.np.ones(list(frame.shape)[:2]) * 0
        frame[:, :, 2] = self.np.ones(list(frame.shape)[:2]) * 0
        return frame

    def __put_color_green(self, frame):
        frame[:, :, 0] = self.np.ones(list(frame.shape)[:2]) * 0
        frame[:, :, 1] = self.np.ones(list(frame.shape)[:2]) * 255
        frame[:, :, 2] = self.np.ones(list(frame.shape)[:2]) * 0
        return frame

    """
        poner imagenes en lienzo
    """

    def poner_titulo(self, frame_titulo):
        if self.__MARGEN_SUPERIOR != 0:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4)
        else:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] / 4)

        if self.__MARGEN_LATERAL != 0:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL)
        else:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1])

        titulo = self.cv2.resize(frame_titulo, (ancho_titulo, alto_titulo))

        origen_x, origen_y = int(self.__MARGEN_SUPERIOR), int(self.__MARGEN_LATERAL)
        end_x, end_y = int(titulo.shape[0] + self.__MARGEN_SUPERIOR), int(titulo.shape[1] + self.__MARGEN_LATERAL)
        self.black_screen[origen_x:end_x, origen_y:end_y] = titulo

    def poner_nombre(self, frame_nombre):
        if self.__MARGEN_SUPERIOR != 0:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4)
        else:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] / 4)

        if self.__MARGEN_LATERAL != 0:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL)
        else:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1])

        margen_superior = self.__MARGEN_SUPERIOR + alto_titulo

        nombre = self.cv2.resize(frame_nombre, (ancho_titulo, alto_titulo))

        origen_x, origen_y = int(margen_superior), int(self.__MARGEN_LATERAL)
        end_x, end_y = int(nombre.shape[0] + margen_superior), int(nombre.shape[1] + self.__MARGEN_LATERAL)
        self.black_screen[origen_x:end_x, origen_y:end_y] = nombre

    def poner_instruccion(self, frame_instruccion):
        if self.__MARGEN_SUPERIOR != 0:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 2)
        else:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] / 2)

        if self.__MARGEN_LATERAL != 0:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL / 2)
        else:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] / 2)

        board_temporal = self.get_board_instruccion()
        board_temporal = self.cv2.resize(board_temporal, (ancho_titulo, alto_titulo))
        board_temporal = self.cv2.resize(board_temporal, (0, 0), fx=self.PORCENTAJE_MARGEN_INSTRUCCION,
                                         fy=self.PORCENTAJE_MARGEN_INSTRUCCION)

        escala_x = frame_instruccion.shape[0] / board_temporal.shape[0]
        escala_y = frame_instruccion.shape[1] / board_temporal.shape[1]
        new_dimen_x = int(frame_instruccion.shape[0] / escala_x), int(frame_instruccion.shape[1] / escala_x)
        new_dimen_y = int(frame_instruccion.shape[0] / escala_y), int(frame_instruccion.shape[1] / escala_y)
        if new_dimen_x[0] <= board_temporal.shape[0] and new_dimen_x[1] <= board_temporal.shape[1]:
            new_dimen = new_dimen_x
        else:
            new_dimen = new_dimen_y
        escala = new_dimen[0] / frame_instruccion.shape[0]

        frame_instruccion = self.cv2.resize(frame_instruccion, (0, 0), fx=escala, fy=escala)

        centro_x = board_temporal.shape[0] / 2
        centro_y = board_temporal.shape[1] / 2
        centro_x_imagen = frame_instruccion.shape[0] / 2
        centro_y_imagen = frame_instruccion.shape[1] / 2

        board_temporal[int(centro_x - centro_x_imagen):int(centro_x + centro_x_imagen),
        int(centro_y - centro_y_imagen):int(centro_y + centro_y_imagen)] = frame_instruccion

        margen_superior = self.__MARGEN_SUPERIOR + alto_titulo
        origen_x, origen_y = int(margen_superior), int(self.__MARGEN_LATERAL)
        end_x, end_y = int(board_temporal.shape[0] + margen_superior), int(
            board_temporal.shape[1] + self.__MARGEN_LATERAL)

        self.black_screen[origen_x:end_x, origen_y:end_y] = board_temporal

    def poner_cronometro(self, frame_cronometro):
        if self.__MARGEN_SUPERIOR != 0:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 2)
        else:
            alto_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[0] / 2)

        if self.__MARGEN_LATERAL != 0:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL / 2)
        else:
            ancho_titulo = int(self.LIENZO_MOSTRAR_VIDEOS[1] / 2)

        board_temporal = self.get_board_cronometro()
        board_temporal = self.cv2.resize(board_temporal, (ancho_titulo, alto_titulo))
        board_temporal = self.cv2.resize(board_temporal, (0, 0), fx=self.PORCENTAJE_MARGEN_CRONOMETRO,
                                         fy=self.PORCENTAJE_MARGEN_CRONOMETRO)

        escala_x = frame_cronometro.shape[0] / board_temporal.shape[0]
        escala_y = frame_cronometro.shape[1] / board_temporal.shape[1]
        new_dimen_x = int(frame_cronometro.shape[0] / escala_x), int(frame_cronometro.shape[1] / escala_x)
        new_dimen_y = int(frame_cronometro.shape[0] / escala_y), int(frame_cronometro.shape[1] / escala_y)
        if new_dimen_x[0] <= board_temporal.shape[0] and new_dimen_x[1] <= board_temporal.shape[1]:
            new_dimen = new_dimen_x
        else:
            new_dimen = new_dimen_y
        escala = new_dimen[0] / frame_cronometro.shape[0]

        frame_cronometro = self.cv2.resize(frame_cronometro, (0, 0), fx=escala, fy=escala)

        centro_x = board_temporal.shape[0] / 2
        centro_y = board_temporal.shape[1] / 2
        centro_x_imagen = frame_cronometro.shape[0] / 2
        centro_y_imagen = frame_cronometro.shape[1] / 2

        board_temporal[int(centro_x - centro_x_imagen):int(centro_x + centro_x_imagen),
        int(centro_y - centro_y_imagen):int(centro_y + centro_y_imagen)] = frame_cronometro

        margen_superior = self.__MARGEN_SUPERIOR + alto_titulo
        margen_lateral = self.__MARGEN_LATERAL + ancho_titulo
        origen_x, origen_y = int(margen_superior), int(margen_lateral)
        end_x, end_y = int(board_temporal.shape[0] + margen_superior), int(board_temporal.shape[1] + margen_lateral)

        self.black_screen[origen_x:end_x, origen_y:end_y] = board_temporal

    """
        get shape bloques
    """

    def get_board_title(self):
        return self.np.zeros([int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4),
                              int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL), 3],
                             dtype=self.np.uint8)

    def get_board_name(self):
        return self.np.zeros([int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4),
                              int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL), 3],
                             dtype=self.np.uint8)

    def get_board_instruccion(self):
        return self.np.zeros([int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4),
                              int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL), 3],
                             dtype=self.np.uint8)

    def get_board_cronometro(self):
        return self.np.zeros([int(self.LIENZO_MOSTRAR_VIDEOS[0] * self.PORCENTAJE_SUPERIOR / 4),
                              int(self.LIENZO_MOSTRAR_VIDEOS[1] * self.PORCENTAJE_LATERAL), 3],
                             dtype=self.np.uint8)

    """
        default value board
    """

    def __default_board_title(self):
        bloque_titulo = self.get_board_title()
        bloque_titulo = self.__put_color_red(bloque_titulo)
        return bloque_titulo.copy()

    def __default_board_name(self):
        bloque_name = self.get_board_name()
        bloque_name = self.__put_color_green(bloque_name)
        return bloque_name.copy()

    def __default_board_instruction(self):
        bloque_instruction = self.get_board_instruccion()
        bloque_instruction = self.__put_color_blue(bloque_instruction)
        return bloque_instruction.copy()

    def __default_board_cronometro(self):
        bloque_cronometro = self.get_board_cronometro()
        bloque_cronometro = self.__put_color_purple(bloque_cronometro)
        return bloque_cronometro.copy()


class Video:
    @staticmethod
    def read():
        return False, None


if __name__ == '__main__':
    from Audiovisual import audiovisual

    video_instruccion = Video()
    cronometro = Video()

    PANTALLAS = dict()
    PANTALLAS['RPI'] = (800, 480)

    SCREEN = "RPI"
    LIENZO_MOSTRAR_VIDEOS = (PANTALLAS[SCREEN][1], PANTALLAS[SCREEN][0])  # pixeles (alto, largo)

    lienzo = Lienzo(LIENZO_MOSTRAR_VIDEOS)
    lienzo.PORCENTAJE_SUPERIOR = 0.9
    lienzo.PORCENTAJE_LATERAL = 0.94
    lienzo.create_board()

    id_audivisual = -1
    delay = True

    while True:
        board = lienzo.get_board()

        hay_image, image = video_instruccion.read()
        if hay_image:
            lienzo.poner_instruccion(image)
        else:
            if delay:
                id_audivisual += 1
                if id_audivisual >= len(audiovisual):
                    id_audivisual = 0
            delay = False if delay else True
            video_instruccion = cv2.VideoCapture(audiovisual[id_audivisual]['video'])


        hay_image, image = cronometro.read()
        if hay_image:
            lienzo.poner_cronometro(image)
        else:
            cronometro = cv2.VideoCapture(audiovisual[id_audivisual]['cronometro'])

        cv2.imshow("Frame", board)
        # ---------------- salida del while al oprimir la tecla ESC
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    video_instruccion.release()
    cv2.destroyAllWindows()
