
docker build -t "nombre_persona:v1" .

docker container run -d -v /home/pi/DATA/history.json:/code/DATA/history.json  -v /home/pi/DATA/BEACON_SCAN.json:/code/DATA/BEACON_SCAN.json  -v /home/pi/DATA/PERSON_SCAN.json:/code/DATA/PERSON_SCAN.json --name=nombre_persona --restart=always  -p 5004:5004  nombre_persona:v1
