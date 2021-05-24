# usando la consola de la raspberry se debe crear el archivo con:
sudo nano /etc/udev/rules.d/99-camera.rules

# Dentro del archivo poner:
SUBSYSTEM=="vchiq",MODE="0666"

# Crear la imagen y el contenedor del docker con:
docker-compose up -d

