docker build -t "vector:v1" .

docker container run -d --name=vector --restart=always -p 5003:5003  vector:v1


