curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo apt-get install -y libffi-dev libssl-dev
sudo pip3 install docker-compose

sudo apt install -y xauth
sudo apt install -y acl
sudo apt install -y x11-apps

chmod +777 /etc/udev/rules.d/

sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:linux-arm

sudo docker pull arm32v7/python

sudo docker pull mcr.microsoft.com/dotnet/runtime

sudo docker pull armindocachada/tensorflow2-opencv4-raspberrypi4