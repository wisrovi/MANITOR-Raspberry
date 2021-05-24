# 1) indicamos la imagen base a usar
#FROM mcr.microsoft.com/dotnet/core/runtime:3.1
FROM arm32v7/python:3.6.13-buster

# 2) creamos una carpeta para alojar los archivos del proyecto
WORKDIR /code

# 3) instalamos sudo y actualizamos
RUN apt update -y
RUN apt-get -y install sudo

# 4) instalar dependencias del SO

# 5) instalar dependencias de python
COPY requirements.txt .
RUN sudo pip3 install -r requirements.txt

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

# 7) le damos permisos a la carpeta donde se alojan los archivos del proyecto para que los archivos python puedan trabajar sin problemas
RUN sudo chmod -R +777 /code

# 8) le decimos que archivo ejecutar cuando se lance el container
#CMD [ "tail" ,"-f", "/etc/hosts" ]
CMD ["python3", "./service.py" ]
