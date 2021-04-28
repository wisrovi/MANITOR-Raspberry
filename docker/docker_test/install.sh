sudo docker build -t "test_mqtt:v1" .

docker container run --privileged -d --name=test_mqtt -p 5001:5001 test_mqtt:v1
