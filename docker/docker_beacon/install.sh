sudo docker pull don41382/rpi-python3-with-bluetooth

sudo docker build -t "beacon_scan:v1" .

docker container run -d --net host --name=beacon_scan beacon_scan:v1
