curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo apt-get install -y libffi-dev libssl-dev
sudo pip3 install docker-compose

sudo apt install -y xauth
sudo apt install -y acl
sudo apt install -y x11-apps

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

sudo chmod -R +777 /home/pi/

chmod +777 /etc/udev/rules.d/

sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:linux-arm

sudo docker pull arm32v7/python:3.6.13-buster

sudo docker pull mcr.microsoft.com/dotnet/runtime:3.1

sudo docker pull armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0