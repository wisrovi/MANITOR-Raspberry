# syntax=docker/dockerfile:1

# para instalar docker en raspberry seguir: https://iotbytes.wordpress.com/setting-up-docker-on-raspberry-pi-and-running-hello-world-container/


# *****************************************************************************************
# *                              choose the base image                                    *
# *           Python Base Image from https://hub.docker.com/r/arm32v7/python/             *
# *****************************************************************************************

FROM arm32v7/python:3.6.13-buster

# *****************************************************************************************
# *                           create folder for copy files project                        *
# *****************************************************************************************

# creamos un directorio de trabajo donde poner los archivos fuente
WORKDIR /code

# *****************************************************************************************
# *                              install packs in OS                                      *
# *****************************************************************************************

# instalar paquetes necesarios en el sistema
RUN apt update -y
RUN apt-get -y install sudo

# otras instalaciones de fuentes en el SO
RUN echo Hola mundo

# *****************************************************************************************
# *                              create new user sudo                                     *
# *****************************************************************************************

# crear el usuario con nombre usuario
RUN useradd -m usuario

# add el usuario al grupo habilitarlo sin contraseña
RUN echo "usuario:grupo" | chpasswd

# adicionar el usuario a sudo
RUN adduser usuario sudo

RUN echo "usuario ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# decirle docker que usuario debe usar para los demas pasos, incluso la ejecusion del proyecto
USER usuario

# *****************************************************************************************
# *                              install python packs                                     *
# *****************************************************************************************

# install dependencies
RUN pip3 install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .
RUN sudo pip3 install -r requirements.txt

# *****************************************************************************************
# *                              copy files project                                       *
# *****************************************************************************************

# Copy the Python Script
# copy only the dependencies installation from the 1st stage image
COPY src .

# update PATH environment variable
# ENV PATH=/root/.local:$PATH

# definir la carpeta a usar para lanzar el proyecto
# CMD /bin/bash

# command to run on container start
CMD [ "sudo" ,"python3", "./test_mqtt.py" ]