# 1) indicamos la imagen base a usar
FROM arm32v7/python:3.6.13-buster

# 2) creamos una carpeta para alojar los archivos del proyecto
WORKDIR /code_brain

# 3) instalamos sudo y actualizamos
RUN echo brain
RUN apt update -y
RUN apt-get -y install sudo

# 4) instalar dependencias del SO
RUN apt-get -y install net-tools

# 5) instalar dependencias de python
RUN pip3 install requests
RUN pip3 install flask

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

# 7) le damos permisos a la carpeta donde se alojan los archivos del proyecto para que los archivos python puedan trabajar sin problemas
RUN chmod -R +777 /code_brain

# 8) le decimos que archivo ejecutar cuando se lance el container
# CMD ["tail","-f","/dev/null"]
CMD ["python3", "./service.py" ]
