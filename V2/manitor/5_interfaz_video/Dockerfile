FROM armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0

WORKDIR /code

RUN echo interfaz_video

RUN export READTHEDOCS=true
RUN pip3 install picamera

RUN apt-get -y install libgtk2.0-dev
RUN rm -rf /tmp/* /usr/share/doc/* /usr/share/info/* /var/tmp/*
RUN apt-get -y install x11-apps

RUN export DISPLAY=:0

RUN pip3 install flask

COPY src .

RUN chmod -R +777 /code

# CMD ["tail","-f","/dev/null"]
CMD ["python3", "./service.py" ]
