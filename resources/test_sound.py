#! /usr/bin/env python
DEVICE = "RPI"
DEVICE = "PC"



from multiprocessing import Process

if DEVICE == "RPI":
    import os
    def audio():
        os.system('omxplayer sound.mp3')
else:
    from playsound import playsound
    def audio():
        playsound("p0.mp3")


Process(target=audio).start()