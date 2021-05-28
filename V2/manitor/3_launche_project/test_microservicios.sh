echo ""
echo ""
echo "microservicio scan card holder"
curl http://localhost:5001/beacons

echo ""
echo ""
echo "microservicio reproducir audio"
curl http://localhost:5002/reproduce?id=0

echo ""
echo ""
echo "microservicio MQTT"
curl http://localhost:5003/mac

echo ""
echo ""
echo "microservicio nombre persona"
curl http://localhost:5004/name

echo ""
echo ""
echo "microservicio interfaz video"
curl http://localhost:5005/

echo ""
echo ""
echo "microservicio movimiento frente a la camara"
curl http://localhost:5006

echo ""
echo ""
echo "microservicio almacenamiento vector"
curl http://localhost:5007

echo ""
echo ""