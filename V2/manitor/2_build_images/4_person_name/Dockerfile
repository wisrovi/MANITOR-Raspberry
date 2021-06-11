# 1) indicamos la imagen base a usar
FROM arm32v7/python:3.6.13-buster

#Author and Maintainer
MAINTAINER wisrovi.rodriguez@gmail.com

# 2) creamos una carpeta para alojar los archivos del proyecto
WORKDIR /code

RUN echo person_name

# 3) instalamos sudo y actualizamos
RUN apt update -y
RUN apt-get -y install sudo

# 4) instalar dependencias del SO

# 5) instalar dependencias de python
RUN pip3 install flask

RUN apt-get -y install net-tools
RUN pip3 install requests

COPY requirements.txt .
RUN sudo pip3 install -r requirements.txt

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

# 7) le damos permisos a la carpeta donde se alojan los archivos del proyecto para que los archivos python puedan trabajar sin problemas
RUN sudo chmod -R +777 /code

# 8) le decimos que archivo ejecutar cuando se lance el container
#CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD ["python3", "./service.py" ]
