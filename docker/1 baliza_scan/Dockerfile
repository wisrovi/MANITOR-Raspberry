# syntax=docker/dockerfile:1

# para instalar docker en raspberry seguir: https://iotbytes.wordpress.com/setting-up-docker-on-raspberry-pi-and-running-hello-world-container/


# *****************************************************************************************
# *                              choose the base image                                    *
# *           Python Base Image from https://hub.docker.com/r/arm32v7/python/             *
# *             https://hub.docker.com/r/don41382/rpi-python3-with-bluetooth/             *
# *****************************************************************************************

#FROM arm32v7/python:3.6.13-buster
#FROM arm32v7/python:3.7.10-stretch
FROM don41382/rpi-python3-with-bluetooth


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
RUN apt-get -y install libbluetooth-dev
RUN apt-get -y install libcap2-bin
RUN apt-get -y install bluez

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
# *                              copy files project                                       *
# *****************************************************************************************

# Copy the Python Script
# copy only the dependencies installation from the 1st stage image
COPY ./src .

# CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD [ "sudo" ,"python3", "./docker_beacon_scan_flask.py" ]
