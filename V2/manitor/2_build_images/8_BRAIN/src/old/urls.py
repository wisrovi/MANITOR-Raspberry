import subprocess
import re


def __getRoute():
    """
    Funcion que devuelve el resultado del comando 'route -n'
    """
    try:
        return subprocess.getoutput("/sbin/route -n").splitlines()
    except:
        return ""


def returnGateway():
    """ Funcion que devuelve la puerta de enlace predeterminada ... """
    # Recorremos todas las lineas de la lista
    for line in __getRoute():
        # Si la primera posicion de la lista empieza 0.0.0.0
        if line.split()[0] == "0.0.0.0":
            # Cogemos la direccion si el formato concuerda con una direccion ip
            if re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$", line.split()[1]):
                return line.split()[1]
    return ''


GATEWAY = returnGateway()


GATEWAY = "192.168.1.106"

URL_SONIDO = 'http://' + GATEWAY + ':5002/reproduce?id='
URL_NAME = 'http://' + GATEWAY + ':5004/name'
URL_VIDEO = 'http://' + GATEWAY + ':5005/mostrar?id=$ID&name='
URL_MOVIMIENTO = 'http://' + GATEWAY + ':5006/move?umbral=$umb'
URL_ENVIA_VECTOR = 'http://' + GATEWAY + ':5007/report'
URL_GUARDA_VECTOR = 'http://' + GATEWAY + ':5007/time?id=$ID&time=$TIME'