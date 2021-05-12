
docker build -t "nombre_persona:v1" .

docker container run -d -v /home/pi/DATA:/code/DATA --name=nombre_persona  -p 5004:5004  nombre_persona:v1
