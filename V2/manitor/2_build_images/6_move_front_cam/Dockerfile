FROM armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0

#Author and Maintainer
MAINTAINER wisrovi.rodriguez@gmail.com

WORKDIR /code_move

RUN echo move_fron_cam

RUN export READTHEDOCS=true
RUN pip3 install picamera

RUN apt-get -y install libgtk2.0-dev
RUN rm -rf /tmp/* /usr/share/doc/* /usr/share/info/* /var/tmp/*
RUN apt-get -y install x11-apps

RUN export DISPLAY=:0

RUN pip3 install flask

COPY src .

RUN touch /static/move.jpg

RUN chmod -R +777 /code_move

# CMD ["tail","-f","/dev/null"]
CMD ["python3", "./service.py" ]
