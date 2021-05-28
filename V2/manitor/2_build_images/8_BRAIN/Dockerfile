FROM arm32v7/python:3.6.13-buster

WORKDIR /code_brain

RUN echo brain

RUN apt update -y
RUN apt-get -y install sudo

RUN apt-get -y install net-tools

RUN pip3 install requests
RUN pip3 install flask

# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

RUN chmod -R +777 /code_brain

CMD ["tail","-f","/dev/null"]
# CMD ["python3", "./service.py" ]
