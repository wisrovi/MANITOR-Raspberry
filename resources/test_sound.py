from multiprocessing import Process

from playsound import playsound

def audio():
    playsound("p0.mp3")




Process(target=audio).start()