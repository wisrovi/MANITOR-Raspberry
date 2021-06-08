class Consult_Microservicios(object):
    from urls import URL_MOVIMIENTO, URL_SONIDO, URL_VIDEO, URL_NAME, URL_GUARDA_VECTOR, URL_ENVIA_VECTOR
    from config import AUDIO_POR_FAVOR_MUEVA_MANOS
    import requests

    import subprocess
    import re

    def __init__(self):
        # TODO: Dejar unicamente returnGateway()
        self.GATEWAY = "192.168.1.109" # self.returnGateway()

    def __getRoute(self):
        """
        Funcion que devuelve el resultado del comando 'route -n'
        """
        try:
            return self.subprocess.getoutput("/sbin/route -n").splitlines()
        except:
            return ""

    def returnGateway(self):
        """ Funcion que devuelve la puerta de enlace predeterminada ... """
        # Recorremos todas las lineas de la lista
        for line in self.__getRoute():
            # Si la primera posicion de la lista empieza 0.0.0.0
            if line.split()[0] == "0.0.0.0":
                # Cogemos la direccion si el formato concuerda con una direccion ip
                if self.re.match("^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})$", line.split()[1]):
                    return line.split()[1]
        return ''

    def __get(self, url):
        r = None
        try:
            r = self.requests.get(url=url)
            data = r.json()
            return data
        except Exception as err:
            if r is not None:
                r = r.text
            print(url, err, r)
            return None

    def get_ip_localhost(self):
        return self.GATEWAY

    def hay_movimiento(self, porcentaje_umbral=30):
        url = self.URL_MOVIMIENTO.replace('$umb', str(porcentaje_umbral))
        movimiento = self.__get(url)

        if movimiento is not None:
            # print("RTA:", movimiento)
            if 'move' in movimiento:
                movimiento = movimiento['move']
                return False if movimiento == 0 else True
            else:
                return False
        else:
            return None

    def mostrar_audiovisual(self, id_audiovisual, nombre):
        try:
            self.__get(self.URL_SONIDO + str(id_audiovisual))
            self.__get(self.URL_VIDEO.replace('$ID', str(id_audiovisual)) + nombre)
        except:
            print(id_audiovisual, nombre)

    def mostrar_video(self, id_audiovisual, nombre):
        self.__get(self.URL_VIDEO.replace('$ID', str(id_audiovisual)) + nombre)

    def leer_nombre_persona(self):
        name_json = self.__get(self.URL_NAME)
        nombre = None
        uuid = None
        if name_json is not None:
            if len(name_json) > 0:
                if 'data' in name_json:
                    data = name_json['data']
                    uuid = [k for k in data.keys()][0]
                    # print(data)
                if 'name' in name_json:
                    nombre = name_json['name']
                    # print("[leer_nombre_persona]: Nombre leido:", nombre, uuid)
        return nombre, uuid

    def guardar_en_vector(self, id_paso:str, tiempo:str):
        url = self.URL_GUARDA_VECTOR.replace("$ID", str(id_paso))
        url = url.replace("$TIME", str(tiempo))
        self.__get(url)

    def reportar_vector(self, uuid, voltaje):
        url = self.URL_ENVIA_VECTOR.replace("$UUID", uuid)
        url = url.replace("$VOLT", str(voltaje))
        rta = self.__get(url)
        print(rta)

    def indicar_audio_mueva_manos(self):
        print("Enviando audio: por favor mueva las manos (audio 11)")
        self.__get(self.URL_SONIDO + str(self.AUDIO_POR_FAVOR_MUEVA_MANOS))


if __name__ == '__main__':
    service = Consult_Microservicios()
    print(service.hay_movimiento(0))
    print(service.leer_nombre_persona())