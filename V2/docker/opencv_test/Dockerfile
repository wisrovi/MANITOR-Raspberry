FROM armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0

WORKDIR /code

RUN export READTHEDOCS=true
RUN pip3 install picamera

COPY src .

RUN chmod -R +777 /code

CMD ["tail","-f","/dev/null"]
