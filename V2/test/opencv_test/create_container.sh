

sudo docker container run --privileged -d  --net host --device=/dev/vchiq -v /dev/bus/usb:/dev/bus/usb -v /tmp/.X11-unix:/tmp/.X11-unix -v /opt/vc:/opt/vc -e LD_LIBRARY_PATH=/opt/vc/lib  --name=base_opencv base_opencv:v1