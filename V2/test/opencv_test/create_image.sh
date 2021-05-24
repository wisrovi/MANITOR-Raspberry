/etc/udev/rules.d/99-camera.rules
SUBSYSTEM=="vchiq",MODE="0666"
xhost +local:

sudo docker build -t "base_opencv:v1" .