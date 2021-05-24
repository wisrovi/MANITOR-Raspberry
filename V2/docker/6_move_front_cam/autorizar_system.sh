chmod +777 /etc/udev/rules.d/
SUBSYSTEM=="vchiq",MODE="0666" >> /etc/udev/rules.d/99-camera.rules