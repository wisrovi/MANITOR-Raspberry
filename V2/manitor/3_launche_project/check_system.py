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
lista_opciones.append(("1_morjarse_manos"))
lista_opciones.append(("2_aplique_jabon"))
lista_opciones.append(("3_palma_con_palma"))
lista_opciones.append(("4_detras_manos"))
lista_opciones.append(("5_entre_dedos"))
lista_opciones.append(("6_detras_dedos"))
lista_opciones.append(("7_pulgares"))
lista_opciones.append(("8_unas"))
lista_opciones.append(("9_munecas"))
lista_opciones.append(("10_enjuaga_seca"))


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

            try:
                url = 'http://' + txt.get() + ':5003/topics'
                rta = get(url)
                OBJ = json.loads(rta[1])
                keys = [k for k in OBJ.keys()]
                if len(keys) > 1:
                    hay_conexion_mqtt.set(True)
                    lbl_mqtt.configure(image=mqtt_ON)
                    lbl_move.image = mqtt_ON
                    acc_mqtt.set("Hay conexion mqtt ({})".format("SI"))
                else:
                    hay_conexion_mqtt.set(False)
                    lbl_mqtt.configure(image=mqtt_OFF)
                    lbl_move.image = mqtt_OFF
                    acc_mqtt.set("Hay conexion mqtt ({})".format("NO"))
            except:
                print('Info', 'No se encontró el microservicio 5003')
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
    messagebox.showinfo('Info', 'IP guardada correctamente')


def clicked_send_audiovisual():
    rta = combo.get()
    id = int(rta[:rta.find("_")])
    print("command", id)

    try:
        url = 'http://' + txt.get() + ':5005/mostrar?id=' + str(id) + "&name=" + name_person.get()
        rta = get(url)
    except:
        print('Info', 'No se encontró el microservicio 5005')

    try:
        url = 'http://' + txt.get() + ':5002/reproduce?id=' + str(id)
        rta = get(url)
    except:
        print('Info', 'No se encontró el microservicio 5002')


def cambio_opcion(event):
    print("New Element Selected", combo.get())


tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='First')
tab_control.add(tab2, text='Second')

# primera pestaña

txt = Entry(tab1)
txt.place(width=200,height=50)
txt.grid(column=1, row=1)
txt.focus()

ip_guardada = BooleanVar()
btn = Button(tab1, text="Guardar ip", command=clicked_btn_save_ip).grid(column=2, row=1)

# segunda pestaña

img_move = ImageTk.PhotoImage(Image.open("mano_move.png").resize((200, 200), Image.ANTIALIAS))
img_no_move = ImageTk.PhotoImage(Image.open("mano_NO_move.png").resize((200, 200), Image.ANTIALIAS))
lbl_move = Label(tab2, image=img_no_move)
lbl_move.grid(column=1, row=3)

mqtt_ON = ImageTk.PhotoImage(Image.open("mqtt_ON.png").resize((200, 200), Image.ANTIALIAS))
mqtt_OFF = ImageTk.PhotoImage(Image.open("mqtt_off.png").resize((200, 200), Image.ANTIALIAS))
lbl_mqtt = Label(tab2, image=mqtt_OFF)
lbl_mqtt.grid(column=2, row=3)

hay_movimiento = BooleanVar()
acc_move = StringVar()
acc_move.set("Hay movimiento")
chk = Checkbutton(tab2, textvar=acc_move, var=hay_movimiento)
chk.grid(column=1, row=4)

hay_conexion_mqtt = BooleanVar()
acc_mqtt = StringVar()
acc_mqtt.set("Hay conexion mqtt")
chk_2 = Checkbutton(tab2, textvar=acc_mqtt, var=hay_conexion_mqtt)
chk_2.grid(column=2, row=4)

combo = Combobox(tab2)
combo['values'] = lista_opciones
combo.current(0)
combo.grid(column=1, row=5)
combo.bind("<<ComboboxSelected>>", cambio_opcion)

btn2 = Button(tab2, text="Activar audiovisual", command=clicked_send_audiovisual).grid(column=2, row=5)

uuid_cardholder = StringVar()
lbl = Label(tab2, textvariable=uuid_cardholder)
lbl.grid(column=1, row=6)

name_person = StringVar()
lbl2 = Label(tab2, textvariable=name_person)
lbl2.grid(column=2, row=6)

tab_control.pack(expand=1, fill='both')
window.mainloop()
