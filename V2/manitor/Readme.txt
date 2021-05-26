# 1) Instalar fuentes en el sistema operativo y descargar imagenes base de docker

sh setup_SO.sh

# 2) para que docker pueda usar la camara escribir en el archivo: sudo nano /etc/udev/rules.d/99-camera.rules

SUBSYSTEM=="vchiq",MODE="0666"

# 3) construir las diferentes imagenes y contenedores del manitor, este comando dentro de la carpeta "manitor"

docker-compose up -d