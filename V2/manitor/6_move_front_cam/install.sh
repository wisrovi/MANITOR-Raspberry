chmod +777 /etc/udev/rules.d/
SUBSYSTEM="vchiq",MODE="0666" >> /etc/udev/rules.d/99-camera.rules

sh build_image.sh

docker container run --privileged -d --device=/dev/vchiq -v /opt/vc:/opt/vc -e LD_LIBRARY_PATH=/opt/vc/lib --name=move_front_cam -p 5006:5006 move_front_cam:v1
#--device=/dev/vcsm
#--device=/dev/vchiq

# sudo docker exec -it move_front_cam bash