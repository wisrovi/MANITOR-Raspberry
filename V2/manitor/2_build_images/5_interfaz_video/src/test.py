# ************************* Tkinter ***********************
from multiprocessing import Process

# from tkinter import PhotoImage
#
# FOLDER = "resources/manos/"
# gifs = list()
# gifs.append(FOLDER + "0_fondo_5fps.gif")
# gifs.append(FOLDER + "1_morjarse_manos_15fps.gif")
# gifs.append(FOLDER + "2_aplique_jabon_5fps.gif")
# gifs.append(FOLDER + "3_palma_con_palma_5fps.gif")
# gifs.append(FOLDER + "4_detras_manos_5fps.gif")
# gifs.append(FOLDER + "5_entre_dedos_5fps.gif")
# gifs.append(FOLDER + "6_detras_dedos_5fps.gif")
# gifs.append(FOLDER + "7_pulgares_5fps.gif")
# gifs.append(FOLDER + "8_unas_5fps.gif")
# gifs.append(FOLDER + "9_munecas_5fps.gif")
# gifs.append(FOLDER + "10_enjuaga_seca_5fps.gif")
#
#
#
# from tkinter import *
#
# root = Tk()
#
# framesNum = 160 # Numero de frames que tiene el gif, si no lo conoces ir haciendo tentativos.
# archivo = FOLDER + "1_morjarse_manos_15fps.gif"
#
# # Lista de todas las imagenes del gif
# frames = [PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(framesNum)]
#
# def update(ind):
#     """ Actualiza la imagen gif """
#     frame = frames[ind]
#     ind += 1
#     if ind == framesNum:
#         ind = 0
#     canvas.create_image(0, 0, image=frame, anchor=NW)
#     root.after(20, update, ind) # Numero que regula la velocidad del gif
#
# canvas = Canvas(width=300, height=100) # Modificar segun el tamaño de la imagen
#
# canvas.pack()
# root.after(0, update, 0)
# root.mainloop()
#
#
#
#
#
# exit()
# frameCnt = 5
# frames = [PhotoImage(file=gifs[0],format = 'gif -index %i' %(i)) for i in range(frameCnt)]
#
# def cargar_frames(file, cantidad_frames):
#     frames = [PhotoImage(file=file, format='gif -index %i' % i) for i in range(cantidad_frames)]
#     return frames
#
# cargar_frames(FOLDER + "1_morjarse_manos_15fps.gif", 5)
#
# import os
# for gif in gifs:
#     if os.path.isfile(gif):
#         for cantidad_frames in range(25):
#             try:
#                 frames = [PhotoImage(file=gif, format='gif -index %i' % i) for i in range(cantidad_frames)]
#             except:
#                 print(gif, cantidad_frames)
#                 break
#     else:
#         print("no file:", gif)
#
# exit()


class Fullscreen_Tkinter:
    import subprocess
    import tkinter as tk
    from tkinter import Canvas, StringVar, BooleanVar, Label, IntVar, NW, PhotoImage, CENTER, YES, BOTH

    width = 800
    height = 480

    FPS = 5

    framesNum = FPS * 3
    framesNum_crono = FPS * 1
    tipo_letra = "Courier"

    def __init__(self):
        self.window = self.tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        # self.__screen_size()

        self.__dividir_lienzo()
        self.__crear_variables()
        self.__create_lienzo_imagen()
        self.crear_elementos()

    def __screen_size(self):
        size = (None, None)
        args = ["xrandr", "-q", "-d", ":0"]
        proc = self.subprocess.Popen(args, stdout=self.subprocess.PIPE)
        for line in proc.stdout:
            if isinstance(line, bytes):
                line = line.decode("utf-8")
                if "Screen" in line:
                    size = (int(line.split()[7]), int(line.split()[9][:-1]))
        return size

    def __get_size_screen(self):
        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.width, self.height = int(width * 0.8), int(height * 0.8)
        print("screen: ", (self.width, self.height))

    def __crear_variables(self):
        self.var_nombre_persona = self.StringVar()
        self.var_nombre_paso = self.StringVar()
        self.var_reiniciar_video = self.BooleanVar()
        self.var_reiniciar_video.set(True)

    def __dividir_lienzo(self):
        self.canvas_global = self.Canvas(self.window, width=self.width, height=self.height, bg="black")
        self.canvas_global.place(relx=0.5, rely=0.5)
        self.canvas_global.pack(expand=self.YES, fill=self.BOTH)

        self.canvas_name = self.Canvas(self.canvas_global, width=self.width, height=int(self.height / 3), bg="black")
        self.canvas_name.pack()

        self.canvas_paso = self.Canvas(self.canvas_global, width=self.width, height=int(self.height / 3), bg="black")
        self.canvas_paso.pack()

        self.canvas_gif = self.Canvas(self.canvas_global, width=self.width, height=int(self.height / 3), bg="black")
        self.canvas_gif.pack()

    def __create_lienzo_imagen(self):
        self.canvas_video_instruccion = self.Canvas(self.canvas_gif, width=360,
                                                    height=360)  # Modificar segun el tamaño de la imagen
        self.canvas_video_instruccion.grid(row=0, column=0)

        self.canvas_crono = self.Canvas(self.canvas_gif, width=360,
                                        height=360)  # Modificar segun el tamaño de la imagen
        self.canvas_crono.grid(row=0, column=1)

    def update_video_instrucion(self, data):
        ind, ind_c = data
        if self.var_reiniciar_video.get():
            ind = 0
            ind_c = 0
            self.var_reiniciar_video.set(False)

        BANDERA_REFRESH = True
        if BANDERA_REFRESH:
            """ Actualiza la imagen gif """
            ind += 1
            if ind >= len(self.frames):
                ind = 0
            frame = self.frames[ind]
            self.canvas_video_instruccion.create_image(0, 0, image=frame, anchor=self.NW)

            """ Actualiza el crono gif """
            ind_c += 1
            if ind_c >= len(self.crono):
                ind_c = 0
            frame = self.crono[ind_c]

            self.canvas_crono.create_image(0, 0, image=frame, anchor=self.NW)

        self.window.after(40, self.update_video_instrucion, (ind, ind_c))  # Numero que regula la velocidad del gif

    def cargar_frames(self, file, cantidad_frames):
        try:
            frames = [self.PhotoImage(file=file, format='gif -index %i' % i) for i in range(cantidad_frames)]
            return frames
        except:
            print(file, cantidad_frames)

    def change_video_instruccion(self, archivo_video, archivo_crono):
        self.frames = self.cargar_frames(archivo_video, self.framesNum)
        self.crono = self.cargar_frames(archivo_crono, self.framesNum_crono)
        self.var_reiniciar_video.set(True)

    def crear_elementos(self):
        label_3 = self.Label(self.canvas_name, text="Bienvenido al Manitor", fg="white", bg="black", anchor=self.CENTER)
        label_3.config(font=(self.tipo_letra, 44))
        label_3.pack()

        self.var_nombre_persona.set("WISROVI")
        label_2 = self.Label(self.canvas_name, textvariable=self.var_nombre_persona, fg="white", bg="black",
                             anchor=self.CENTER)
        label_2.config(font=(self.tipo_letra, 35))
        label_2.pack()

        self.var_nombre_paso.set("paso 1")
        label_4 = self.Label(self.canvas_paso, textvariable=self.var_nombre_paso, fg="white", bg="black",
                             anchor=self.CENTER)
        label_4.config(font=(self.tipo_letra, 35))
        label_4.pack()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)

    def launcher(self):
        self.window.after(0, self.update_video_instrucion, (0, 0))
        self.window.mainloop()

    def set_nombre_persona(self, nombre):
        self.var_nombre_persona.set(nombre)

    def set_nombre_paso(self, nombre):
        self.var_nombre_paso.set(nombre)


class Interfaz_visual(Fullscreen_Tkinter):
    import threading
    from multiprocessing import Queue
    import time

    def __init__(self):
        super().__init__()
        self.__cargar_todos_videos()
        self.var_id_video_gif = self.IntVar()
        self.var_id_video_gif_last = self.IntVar()

        self.mostrar_video(0)

        self.pqueue = self.Queue()

        self.threading.Thread(target=self.check_new_video).start()

    def check_new_video(self):
        while True:
            datos_url_dict = self.leer_cola()
            if len(datos_url_dict) > 0:
                id = datos_url_dict.get('id')
                name = datos_url_dict.get('name')

                self.set_nombre_persona(name)
                self.set_id_video_gif(id)
                self.set_nombre_paso(self.textos[str(id)])

            if self.var_id_video_gif_last.get() != self.var_id_video_gif.get():
                if self.var_id_video_gif.get() < len(self.listado_todos_videos_gif):
                    self.var_id_video_gif_last.set(self.var_id_video_gif.get())
                    if self.var_id_video_gif.get() == 0:
                        self.mostrar_video(self.var_id_video_gif.get(), 0)
                    else:
                        self.mostrar_video(self.var_id_video_gif.get())
            self.time.sleep(0.1)

    def __cargar_todos_videos(self):
        self.textos = dict()
        self.textos['0'] = ""
        self.textos['1'] = "Moje ambas manos con agua"
        self.textos['2'] = "aplique abundante jabón"
        self.textos['3'] = "frote ambas palmas vigorosamente"
        self.textos['4'] = "frote el dorso de cada mano"
        self.textos['5'] = "frote ambas palmas con los dedos entrelazados"
        self.textos['6'] = "frote el dorso de los dedos con las palmas de la manos"
        self.textos['7'] = "frote el dedo pulgar"
        self.textos['8'] = "frote la punta de los dedos con las palmas"
        self.textos['9'] = "frote cada muñeca con la mano opuesta"
        self.textos['10'] = "es el momento de enjuagarse las manos"

        FOLDER = "resources/manos/"
        self.gifs = list()
        self.gifs.append(FOLDER + "0_fondo.gif")
        self.gifs.append(FOLDER + "1_morjarse_manos_10fps.gif")
        self.gifs.append(FOLDER + "2_aplique_jabon_5fps.gif")
        self.gifs.append(FOLDER + "3_palma_con_palma_5fps.gif")
        self.gifs.append(FOLDER + "4_detras_manos_5fps.gif")
        self.gifs.append(FOLDER + "5_entre_dedos_5fps.gif")
        self.gifs.append(FOLDER + "6_detras_dedos_5fps.gif")
        self.gifs.append(FOLDER + "7_pulgares_5fps.gif")
        self.gifs.append(FOLDER + "8_unas_5fps.gif")
        self.gifs.append(FOLDER + "9_munecas_15fps.gif")
        self.gifs.append(FOLDER + "10_enjuaga_seca_5fps.gif")

        self.listado_todos_videos_gif = list()
        for gif in self.gifs:
            frames = self.cargar_frames(gif, self.framesNum)
            if frames is not None:
                self.listado_todos_videos_gif.append(frames)

        FOLDER = "resources/crono/"
        self.listado_todos_crono_gif = list()
        self.listado_todos_crono_gif.append(self.cargar_frames("resources/manos/0_fondo.gif", self.framesNum))
        self.listado_todos_crono_gif.append(self.cargar_frames(FOLDER + "1_seg_cronometro_5fps.gif", self.framesNum_crono))

    def mostrar_video(self, id_video, id_crono=1):
        self.frames = self.listado_todos_videos_gif[id_video]
        self.crono = self.listado_todos_crono_gif[id_crono]
        self.var_reiniciar_video.set(True)

    def set_id_video_gif(self, id):
        self.var_id_video_gif.set(id)

    def leer_cola(self):
        if not self.pqueue.empty():
            data_complete = dict()
            for _ in range(self.pqueue.qsize()):
                data = self.pqueue.get()
                for key, value in data.items():
                    # print(key, value)
                    data_complete[key] = value
            return data_complete
        else:
            return dict()

    def save_cola(self, data_dict):
        self.pqueue.put(data_dict)


app = Interfaz_visual()

# ************************* Flask ***********************
import threading

from flask import Flask, request, json

app_flask = Flask(__name__)


@app_flask.route('/')
def hola():
    return 'Reproduce audio by Wisrovi'


@app_flask.route('/mostrar', methods=['GET'])
def mostrar():
    id = request.args.get('id')
    name = request.args.get('name')

    if id is not None and name is not None:
        OBJ = dict()
        OBJ['id'] = id
        OBJ['name'] = name
        app.save_cola(OBJ)
        return json.dumps(OBJ, indent=4)

    return "no hay dados ingresados, por favor consulte /help las opciones de variables a usar"


def proceso():
    app_flask.run(host="0.0.0.0", port=5005)


if __name__ == '__main__':
    t = threading.Thread(target=proceso)
    t.setDaemon(True)
    t.start()
    # Process(target=proceso).start()

    app.launcher()



