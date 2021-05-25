if [ -d /home ];
then
echo "Carpeta /home ya existe."
else
echo "Creando carpeta /home"
mkdir /home
chmod -R +777 /home
fi

if [ -d /home/pi ];
then
echo "Carpeta /home/pi ya existe."
else
echo "Creando carpeta /home/pi"
mkdir /home/pi
chmod -R +777 /home/pi
fi

if [ -d /home/pi/DATA ];
then
echo "Carpeta /home/pi/DATA ya existe."
else
echo "Creando carpeta /home/pi/DATA"
mkdir /home/pi/DATA
chmod -R +777 /home/pi/DATA
fi

if [ -f /home/pi/DATA/history.json ];
then
echo "Archivo history.json ya existe."
else
echo "Creando archivo history.json."
touch /home/pi/DATA/history.json && chmod +777 /home/pi/DATA/history.json
fi

if [ -f /home/pi/DATA/BEACON_SCAN.json ];
then
echo "Archivo BEACON_SCAN.json ya existe."
else
echo "Creando archivo BEACON_SCAN.json."
touch /home/pi/DATA/BEACON_SCAN.json && chmod +777 /home/pi/DATA/BEACON_SCAN.json
fi

if [ -f /home/pi/DATA/PERSON_SCAN.json ];
then
echo "Archivo PERSON_SCAN.json ya existe."
else
echo "Creando archivo PERSON_SCAN.json."
touch /home/pi/DATA/PERSON_SCAN.json && chmod +777 /home/pi/DATA/PERSON_SCAN.json
fi

sudo apt install xauth
sudo apt install acl
sudo apt install x11-apps

sudo docker build -t "manitor_beacon_scan:latest" "1_baliza_scan"
sudo docker build -t "manitor_reproduce_audio:latest" "2_reproduce_audio"
sudo docker build -t "manitor_send_mqtt:latest" "3_send_mqtt"
sudo docker build -t "manitor_nombre_persona:latest" "4_person_name"
sudo docker build -t "manitor_interfaz_video:latest" "5_interfaz_video"
sudo docker build -t "manitor_move_front_cam:latest" "6_move_front_cam"
sudo docker build -t "manitor_vector:latest" "7_vector"