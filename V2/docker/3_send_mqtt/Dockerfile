# syntax=docker/dockerfile:1

# para instalar docker en raspberry seguir: https://iotbytes.wordpress.com/setting-up-docker-on-raspberry-pi-and-running-hello-world-container/


# *****************************************************************************************
# *                              choose the base image                                    *
# *           Python Base Image from https://hub.docker.com/r/arm32v7/python/             *
# *             https://volkanpaksoy.com/archive/2019/12/05/Using-Audio-in-Docker-Container/             *
# *****************************************************************************************

FROM mcr.microsoft.com/dotnet/core/runtime:3.1


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
RUN echo Instalando nuevos paquetes
RUN apt-get install mpg123 -y
RUN apt-get install python3-pip -y

# otras instalaciones de fuentes en el SO
RUN echo Paquetes instalados




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
# RUN sudo pip3 install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .
RUN sudo pip3 install -r requirements.txt


# *****************************************************************************************
# *                              copy files project                                       *
# *****************************************************************************************

# Copy the Python Script
# copy only the dependencies installation from the 1st stage image
COPY src .
RUN sudo chmod -R +777 /code

#CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD ["python3", "./service.py" ]
