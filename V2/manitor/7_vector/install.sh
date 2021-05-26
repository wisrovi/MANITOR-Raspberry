docker build -t "vector:v1" .

var=$(cat /sys/class/net/eth0/address)

docker container run -d -e MAC_CLIENT=$var --name=vector --link send_mqtt_home_1884:send_mqtt --restart=always -p 5007:5007  vector:v1


