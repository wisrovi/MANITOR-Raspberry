class Consult_Microservicios(object):
    from urls import URL_MOVIMIENTO, URL_SONIDO, URL_VIDEO, URL_NAME, URL_GUARDA_VECTOR, URL_ENVIA_VECTOR
    from config import AUDIO_POR_FAVOR_MUEVA_MANOS
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

    def mostrar_video(self, id_audiovisual, nombre):
        self.__get(self.URL_VIDEO.replace('$ID', str(id_audiovisual)) + nombre)

    def leer_nombre_persona(self):
        name_json = self.__get(self.URL_NAME)
        nombre = None
        uuid = None
        if name_json is not None:
            if len(name_json) > 0:
                uuid = [f for f in name_json][0]
                name_json = name_json[uuid]
                print(name_json)
                if 'name' in name_json:
                    nombre = name_json['name']
        return nombre, uuid

    def guardar_en_vector(self, id_paso:str, tiempo:str):
        url = self.URL_GUARDA_VECTOR.replace("$ID", str(id_paso))
        url = url.replace("$TIME", str(tiempo))
        self.__get(url)

    def reportar_vector(self, uuid, voltaje):
        url = self.URL_ENVIA_VECTOR.replace("$UUID", uuid)
        url = url.replace("$VOLT", str(voltaje))
        self.__get(url)

    def indicar_audio_mueva_manos(self):
        self.__get(self.URL_SONIDO + str(self.AUDIO_POR_FAVOR_MUEVA_MANOS))


if __name__ == '__main__':
    service = Consult_Microservicios()
    print(service.hay_movimiento(0))
    print(service.leer_nombre_persona())