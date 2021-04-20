# para instalar docker en raspberry seguir: https://iotbytes.wordpress.com/setting-up-docker-on-raspberry-pi-and-running-hello-world-container/

# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3.6.13-buster

# Copy the Python Script to beacon scan
COPY docker_beacon_scan.py ./

# Intall the rpi.gpio python module
RUN pip3 install --no-cache-dir PyBluez==0.23
