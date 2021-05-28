



# https://pimylifeup.com/raspberry-pi-docker/

# descarga e instala docker
curl -sSL https://get.docker.com | sh


# configurar docker con el usuario Pi de raspberry
sudo usermod -aG docker pi

# reiniciar para aplicar cambios al usuario pi
logout

# ver version
docker --version


sudo apt-get install libffi-dev libssl-dev
sudo pip3 install docker-compose


# probar primer container
docker run hello-world

# respuesta:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.



