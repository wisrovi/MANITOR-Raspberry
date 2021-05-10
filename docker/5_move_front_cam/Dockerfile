# syntax=docker/dockerfile:1

# para instalar docker en raspberry seguir: https://iotbytes.wordpress.com/setting-up-docker-on-raspberry-pi-and-running-hello-world-container/


# *****************************************************************************************
# *                              choose the base image                                    *
# *           Python Base Image from https://hub.docker.com/r/arm32v7/python/             *
# *****************************************************************************************
#FROM imelnik/rpi-python3-tensorflow-opencv
#FROM python:3
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

RUN sudo apt-get install -y python3
RUN sudo apt-get install -y python3-pip
RUN sudo apt-get install -y python3-dev

RUN sudo apt-get install -y libhdf5-dev
RUN sudo apt-get install -y libhdf5-serial-dev

RUN sudo apt-get install -y libatlas-base-dev
RUN sudo apt-get install -y libatlas-base-dev gfortran

RUN sudo apt-get install -y libqtgui4
RUN sudo apt-get install -y libhdf5-dev
RUN sudo apt-get install -y libhdf5-serial-dev
RUN sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
RUN sudo apt-get install -y libfontconfig1-dev
RUN sudo apt-get install -y libcairo2-dev
RUN sudo apt-get install -y libx264-dev
RUN sudo apt-get install -y libxvidcore-dev
RUN sudo apt-get install -y libv4l-dev
RUN sudo apt-get install -y libavformat-dev
RUN sudo apt-get install -y libswscale-dev
RUN sudo apt-get install -y libavcodec-dev
RUN sudo apt-get install -y libpng-dev
RUN sudo apt-get install -y libjpeg-dev
RUN sudo apt-get install -y libtiff5-dev
RUN sudo apt-get install -y libqt4-test
RUN sudo apt-get install -y ibgtk2.0-dev

RUN sudo apt-get install -y libtbb-dev
RUN sudo apt-get install -y qt5-default
RUN sudo apt-get install -y libvorbis-dev
RUN sudo apt-get install -y libxvidcore-dev
RUN sudo apt-get install -y libx264-dev
RUN sudo apt-get install -y libopencore-amrwb-dev
RUN sudo apt-get install -y x264 v4l-utils

RUN apt-get -y autoremove

# otras instalaciones de fuentes en el SO
RUN echo Hola mundo

# *****************************************************************************************
# *                              create new user sudo                                     *
# *****************************************************************************************

# crear el usuario con nombre usuario
#RUN useradd -m usuario
#
## add el usuario al grupo habilitarlo sin contraseña
#RUN echo "usuario:grupo" | chpasswd
#
## adicionar el usuario a sudo
#RUN adduser usuario sudo
#
#RUN echo "usuario ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
#
## decirle docker que usuario debe usar para los demas pasos, incluso la ejecusion del proyecto
#USER usuario

# *****************************************************************************************
# *                              install python packs                                     *
# *****************************************************************************************

# install dependencies
# RUN pip3 install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .
RUN sudo pip3 install numpy
RUN pip install --upgrade pip setuptools wheel
RUN sudo pip3 install opencv-python
RUN sudo pip3 install -r requirements.txt

# *****************************************************************************************
# *                              copy files project                                       *
# *****************************************************************************************

# Copy the Python Script
# copy only the dependencies installation from the 1st stage image
COPY ./src .

RUN sudo chmod -R +777 /code

# update PATH environment variable
# ENV PATH=/root/.local:$PATH

# definir la carpeta a usar para lanzar el proyecto
# CMD /bin/bash

# command to run on container start
#CMD [ "sudo" ,"python3", "./test_mqtt.py" ]
#CMD [ "python3", "./service.py" ]
#CMD [ "python", "./my_script.py" ]
CMD [ "tail" ,"-f", "/etc/hosts" ]