class Consult_Microservicios(object):
    from urls import URL_MOVIMIENTO, URL_SONIDO, URL_VIDEO, URL_NAME
    from config import pasos, WAIT_TIME, PENALITY_TIME
    import requests

    def __get(self, url):
        try:
            r = self.requests.get(url=url)
            data = r.json()
            return data
        except Exception as err:
            print(err)
            print(url)
            return None

    def hay_movimiento(self, porcentaje_umbral=30):
        url = self.URL_MOVIMIENTO.replace('$umb', str(porcentaje_umbral))
        movimiento = self.__get(url)

        if movimiento is not None:
            print("RTA:", movimiento)
            if 'move' in movimiento:
                movimiento = movimiento['move']
                return False if movimiento == 0 else True
            else:
                return False
        else:
            return False

    def mostrar_audiovisual(self, id_audiovisual, nombre):
        self.__get(self.URL_SONIDO + str(id_audiovisual))
        self.__get(self.URL_VIDEO.replace('$ID', str(id_audiovisual)) + nombre)

    def leer_nombre_persona(self):
        name_json = self.__get(self.URL_NAME)
        nombre = None
        if name_json is not None:
            if len(name_json) > 0:
                uuid = [f for f in name_json][0]
                name_json = name_json[uuid]
                print(name_json)
                if 'name' in name_json:
                    nombre = name_json['name']
        return nombre


if __name__ == '__main__':
    service = Consult_Microservicios()
    print(service.hay_movimiento(0))
    print(service.leer_nombre_persona())