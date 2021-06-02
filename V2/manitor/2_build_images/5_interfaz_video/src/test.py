# video_name = "resources/manos/1_morjarse_manos_15fps.mp4"
#
# from tkinter import *
# from tkvideo import tkvideo
#
# root = Tk()
# my_label = Label(root)
# my_label.pack()
# player = tkvideo(video_name, my_label, loop = 1, size = (1280,720))
# player.play()
#
# root.mainloop()
#
# exit()


from tkinter import *

root = Tk()

framesNum = 24*3 # Numero de frames que tiene el gif, si no lo conoces ir haciendo tentativos.


# Lista de todas las imagenes del gif
archivo = "resources/manos/paso1.gif"
frames = [PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(framesNum)]

def update(ind):
    """ Actualiza la imagen gif """
    frame = frames[ind]
    ind += 1
    if ind == framesNum:
        ind = 0
    canvas.create_image(0, 0, image=frame, anchor=NW)
    root.after(20, update, ind) # Numero que regula la velocidad del gif

canvas = Canvas(width=300, height=100) # Modificar segun el tamaño de la imagen

canvas.pack()
root.after(0, update, 0)
root.mainloop()





exit()


import tkinter as tk


class Fullscreen_Example:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        self.crear_elementos()

        self.window.mainloop()

    def crear_elementos(self):
        pass

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes("-fullscreen", self.fullScreenState)


if __name__ == '__main__':
    app = Fullscreen_Example()

