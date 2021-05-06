chmod +777 /etc/udev/rules.d/
SUBSYSTEM=="vchiq",MODE="0666" >> /etc/udev/rules.d/99-camera.rules

sudo docker build -t "move_front_cam:v1" .

docker container run --privileged -d -v /opt/vc:/opt/vc -e LD_LIBRARY_PATH=/opt/vc/lib --name=move_front_cam -p 5006:5006 move_front_cam:v1
#--device=/dev/vcsm
#--device=/dev/vchiq