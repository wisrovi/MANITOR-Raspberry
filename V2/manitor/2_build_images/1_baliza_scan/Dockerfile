# 1) indicamos la imagen base a usar
FROM arm32v7/python:3.6.13-buster

#Author and Maintainer
MAINTAINER wisrovi.rodriguez@gmail.com

# 2) creamos una carpeta para alojar los archivos del proyecto
WORKDIR /code

RUN echo baliza_scan

# 3) instalamos sudo y actualizamos
RUN apt-get update -y
RUN apt-get -y install sudo

# 4) instalar dependencias del SO
RUN apt-get -y install libbluetooth-dev
RUN apt-get -y install libcap2-bin
RUN apt-get -y install bluez

RUN apt-get -y install libglib2.0-dev
RUN apt-get -y install libbluetooth-dev
RUN apt-get -y install libboost-python-dev

# 5) instalar dependencias de python
RUN pip3 install flask

COPY requirements.txt .
RUN sudo pip3 install -r requirements.txt

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

# 7) le damos permisos a la carpeta donde se alojan los archivos del proyecto para que los archivos python puedan trabajar sin problemas
RUN sudo chmod -R +777 /code

# 8) le decimos que archivo ejecutar cuando se lance el container
# CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD [ "sudo" ,"python3", "./service.py" ]
