# https://pimylifeup.com/raspberry-pi-portainer/

# install
sudo docker pull portainer/portainer-ce:linux-arm


# lanzar
sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:linux-arm

