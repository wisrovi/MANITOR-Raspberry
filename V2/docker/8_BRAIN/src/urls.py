GATEWAY = "localhost"
GATEWAY = "192.168.1.106"

URL_SONIDO = 'http://' + GATEWAY + ':5002/reproduce?id='
URL_NAME = 'http://' + GATEWAY + ':5004/name'
URL_VIDEO = 'http://' + GATEWAY + ':5005/mostrar?id=$ID&name='
URL_MOVIMIENTO = 'http://' + GATEWAY + ':5006/move?umbral=$umb'
URL_ENVIA_VECTOR = 'http://' + GATEWAY + ':5007/report'