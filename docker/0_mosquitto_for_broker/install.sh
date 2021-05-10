# https://www.returngis.net/2019/02/publicar-tu-imagen-en-docker-hub/


docker build -t "mosquitto_broker:v1" .

docker container run -d --name=mosquitto_broker --restart=always -p 1883:1884  mosquitto_broker:v1
