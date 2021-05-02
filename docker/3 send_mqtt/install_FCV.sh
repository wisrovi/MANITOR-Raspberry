
docker build -t "send_mqtt:v1" .

var=$(cat /sys/class/net/eth0/address)

docker container run -d -e MAC_CLIENT=$var -e IP_BROKER=172.30.19.92 -e PORT_BROKER=1883 -e NAME_CLIENT=RPI --name=send_mqtt_home_1885  -p 5003:5003  send_mqtt:v1

#docker container run -d -e MAC_CLIENT=$var -e USER_BROKER=user  -e PASSWORD_BROKER=password  -e IP_BROKER=172.30.19.92 -e PORT_BROKER=1883 -e NAME_CLIENT=RPI --name=send_mqtt_home_1885  -p 5003:5003  send_mqtt:v1
