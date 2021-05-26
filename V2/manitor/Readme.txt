# 0) Aumentar la memoria swap
sudo nano /etc/dphys-swapfile

# 0.1) Buscar la linea: CONF_SWAPSIZE=100, y cambiarla por
CONF_SWAPSIZE=512

# 0.2) Reiniciar la swap:
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# 1) Instalar fuentes en el sistema operativo y descargar imagenes base de docker

sh setup_SO.sh

# 2) para que docker pueda usar la camara escribir en el archivo: sudo nano /etc/udev/rules.d/99-camera.rules

SUBSYSTEM=="vchiq",MODE="0666"

# 3) crear las imagenes de los microservicios, este comando dentro de la carpeta "manitor"

sudo sh recreate_images.sh

# 4) construir los diferentes contenedores del manitor, este comando dentro de la carpeta "manitor"

docker-compose up -d