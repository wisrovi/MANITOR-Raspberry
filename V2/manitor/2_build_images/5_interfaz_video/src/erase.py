# size_original = (39, 320, 569, 3)
#
#
# import numpy as np
# x = np.arange(39* 320* 569* 3).reshape(size_original)
# print(x.shape)
#
#
# a = np.array(list(np.ravel(x)))
# print(a.shape)
#
#
# np.savetxt('test.txt', a)
#
# a = np.loadtxt('test.txt')
#
#
# y = a.reshape(size_original)
# print(y.shape)
#
#

archivo = "resources/manos/2_aplique_jabon_15fps.gif"
archivo = "resources/manos/paso1.gif"

from tkinter import *
import time
import os
root = Tk()

frameCnt = 24*3
frames = [PhotoImage(file=archivo,format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()


exit()
import gif2numpy
import cv2
import time
import numpy as np
from tempfile import TemporaryFile
outfile = TemporaryFile()


def Loading_gif(path):
    print(path)
    np_frames_tempo, extensions, image_specifications = gif2numpy.convert(path)
    return np_frames_tempo


imagenes = list()
#imagenes.append(Loading_gif("resources/manos/1_morjarse_manos_15fps.gif"))
#imagenes.append(Loading_gif("resources/manos/2_aplique_jabon_15fps.gif"))
imagenes.append(Loading_gif("resources/manos/3_palma_con_palma_15fps.gif"))


for frames_imagen in imagenes:
    for img in frames_imagen:
        cv2.imshow("test", img)

        time.sleep(0.025)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
