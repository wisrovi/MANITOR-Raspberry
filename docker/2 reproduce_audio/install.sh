
docker build -t "reproduce__audio:v1" .

docker container run -d --device /dev/snd --name=reproduce__audio  -p 5002:5002  reproduce__audio:v1
