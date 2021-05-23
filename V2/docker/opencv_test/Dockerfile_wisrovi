FROM arm32v7/python:3.6.13-buster
WORKDIR /code
RUN apt update -y
RUN apt-get -y install sudo
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install cmake
RUN sudo apt-get -y install pkg-config
RUN sudo apt-get -y install libjpeg-dev
RUN sudo apt-get -y install libtiff5-dev
#RUN sudo apt-get -y install libjasper-dev
RUN sudo apt-get -y install libpng-dev
RUN sudo apt-get -y install libavcodec-dev
RUN sudo apt-get -y install libavformat-dev
RUN sudo apt-get -y install libswscale-dev
RUN sudo apt-get -y install libv4l-dev
RUN sudo apt-get -y install libxvidcore-dev
RUN sudo apt-get -y install libx264-dev
RUN sudo apt-get -y install libfontconfig1-dev
RUN sudo apt-get -y install libcairo2-dev
RUN sudo apt-get -y install libgdk-pixbuf2.0-dev
RUN sudo apt-get -y install libpango1.0-dev
RUN sudo apt-get -y install libgtk2.0-dev
RUN sudo apt-get -y install libgtk-3-dev
RUN sudo apt-get -y install libatlas-base-dev
RUN sudo apt-get -y install gfortran
RUN sudo apt-get -y install libhdf5-dev
RUN sudo apt-get -y install libhdf5-serial-dev
RUN sudo apt-get -y install libhdf5-103
RUN sudo apt-get -y install libqtgui4
RUN sudo apt-get -y install libqtwebkit4
RUN sudo apt-get -y install libqt4-test
RUN sudo apt-get -y install python3-pyqt5
RUN apt-get update -y
RUN echo "hola mundo"
RUN pip install numpy
RUN pip install pandas

RUN pip install opencv-python
RUN pip install flask
RUN export READTHEDOCS=true
RUN export DISPLAY=:10.0
# RUN pip install "picamera[array]"
# RUN pip install picamera




COPY src .

RUN sudo chmod -R +777 /code

CMD [ "tail" ,"-f", "/etc/hosts" ]


