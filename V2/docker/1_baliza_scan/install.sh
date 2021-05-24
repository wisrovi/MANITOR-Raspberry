
sudo sh system_install.sh

sh build_image.sh

echo **************************** lanzando contenedor ****************************

docker container run --privileged -d --net host --name=beacon_scan  --restart=always beacon_scan:v1
