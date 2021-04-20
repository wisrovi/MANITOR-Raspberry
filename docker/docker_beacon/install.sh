sudo mkdir /home/Beacon
sudo chmod -R 777 /home/Beacon

docker build -t "docker_beacon_scan:v1" .

docker container run --privileged -d docker_beacon_scan:v1