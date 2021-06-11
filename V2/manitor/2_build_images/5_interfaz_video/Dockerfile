FROM armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0

#Author and Maintainer
MAINTAINER wisrovi.rodriguez@gmail.com

WORKDIR /code_video

RUN echo interfaz_video

RUN apt-get update

RUN export READTHEDOCS=true
RUN pip3 install picamera

RUN apt-get -y install python3-tk
RUN apt-get -y install ffmpeg
RUN apt-get -y install libgtk2.0-dev

RUN apt-get -y install x11-xserver-utils
RUN rm -rf /tmp/* /usr/share/doc/* /usr/share/info/* /var/tmp/*
RUN apt-get -y install x11-apps

RUN export DISPLAY=:0

RUN pip3 install flask


# 6) copiamos la carpeta del codigo y todos sus recursos
COPY src .

RUN chmod -R +777 /code_video

# CMD ["tail","-f","/dev/null"]
CMD ["python3", "./test.py" ]
# CMD ["python3", "./service.py" ]
