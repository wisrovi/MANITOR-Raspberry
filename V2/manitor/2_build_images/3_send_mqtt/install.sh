sh build_image.sh

docker container run -d -e MAC_CLIENT=$var -e IP_BROKER=192.168.1.112 -e PORT_BROKER=1884 -e NAME_CLIENT=RPI --name=send_mqtt_home_1883 --restart=always -p 5003:5003  send_mqtt:v1

#docker container run -d -e MAC_CLIENT=$var -e USER_BROKER=user  -e PASSWORD_BROKER=password  -e IP_BROKER=192.168.1.112 -e PORT_BROKER=1885 -e NAME_CLIENT=RPI --name=send_mqtt_home_1885  -p 5003:5003  send_mqtt:v1

