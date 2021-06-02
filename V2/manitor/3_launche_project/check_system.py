import threading
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk
import time
import json
from PIL import ImageTk, Image

import requests

lista_opciones = list()
lista_opciones.append(1)
lista_opciones.append(5)
lista_opciones.append("a")


def get(url):
    DATA = requests.get(url, params={}, timeout=10)
    status_code = DATA.status_code
    text = DATA.text
    return status_code, text


def proceso():
    while True:
        time.sleep(2)

        if ip_guardada.get():
            try:
                url = 'http://' + txt.get() + ':5006/move'
                rta = get(url)
                if rta[1].find("move"):
                    if json.loads(rta[1])['move'] == 1:
                        hay_movimiento.set(True)
                        lbl_move.configure(image=img_move)
                        lbl_move.image = img_move
                    else:
                        hay_movimiento.set(False)
                        lbl_move.configure(image=img_no_move)
                        lbl_move.image = img_no_move

                    acc_move.set("Hay movimiento ({})".format(json.loads(rta[1])['acc']))
            except:
                print('Info', 'No se encontró el microservicio 5006')

            try:
                url = 'http://' + txt.get() + ':5004/mirror'
                rta = get(url)
                if rta[1].find("near"):
                    uuid_cardholder.set([k for k in json.loads(rta[1])['near'].keys()][0])
            except:
                print('Info', 'No se encontró el microservicio 5004')

            try:
                url = 'http://' + txt.get() + ':5004/names'
                rta = get(url)
                if len(rta[1]) > 10:
                    OBJ = json.loads(rta[1])
                    for k, v in OBJ.items():
                        if uuid_cardholder.get() == k:
                            name_person.set(v)
            except:
                print('Info', 'No se encontró el microservicio 5004')
        else:
            print('Info', 'Configure IP')


t = threading.Thread(target=proceso)
t.start()

window = Tk()
window.title("Manitor app")
window.geometry('450x400')
window.resizable(False, False)


def clicked_btn_save_ip():
    print("command", txt.get())
    hay_movimiento.set(False)
    name_person.set("")
    ip_guardada.set(True)
    # messagebox.showinfo('Message title', 'Message content')


def clicked_send_audiovisual():
    print("command", combo.get())

    try:
        url = 'http://' + txt.get() + ':5005/mostrar?id=' + combo.get() + "&name=" + name_person.get()
        rta = get(url)
    except:
        print('Info', 'No se encontró el microservicio 5005')

    try:
        url = 'http://' + txt.get() + ':5002/reproduce?id=' + combo.get()
        rta = get(url)
    except:
        print('Info', 'No se encontró el microservicio 5002')


def cambio_opcion(event):
    print("New Element Selected")


tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='First')
tab_control.add(tab2, text='Second')

# primera pestaña

txt = Entry(tab1, width=10)
txt.grid(column=1, row=1)
txt.focus()

ip_guardada = BooleanVar()
btn = Button(tab1, text="Guardar ip", command=clicked_btn_save_ip).grid(column=2, row=1)

# segunda pestaña

img_move = ImageTk.PhotoImage(Image.open("mano_move.png"))
img_no_move = ImageTk.PhotoImage(Image.open("mano_NO_move.png"))
lbl_move = Label(tab2, image=img_move)
lbl_move.grid(column=1, row=3)

hay_movimiento = BooleanVar()
acc_move = StringVar()
acc_move.set("Hay movimiento")
chk = Checkbutton(tab2, textvar=acc_move, var=hay_movimiento)
chk.grid(column=1, row=4)

uuid_cardholder = StringVar()
lbl = Label(tab2, textvariable=uuid_cardholder)
lbl.grid(column=1, row=5)

name_person = StringVar()
lbl2 = Label(tab2, textvariable=name_person)
lbl2.grid(column=2, row=5)

combo = Combobox(tab2)
combo['values'] = lista_opciones
combo.current(1)
combo.grid(column=1, row=6)
combo.bind("<<ComboboxSelected>>", cambio_opcion)

btn2 = Button(tab2, text="Activar audiovisual", command=clicked_send_audiovisual).grid(column=2, row=6)

tab_control.pack(expand=1, fill='both')
window.mainloop()
