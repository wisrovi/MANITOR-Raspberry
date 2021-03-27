
def main_move_detect():
    import cv2
    import time
    from DetectMoveSkinUtil import Deteccion_movimiento

    class Proceso_deteccion_movimiento(object):
        import time

        time_elapsed = float()

        def iniciar_proceso(self):
            print("Proceso iniciado")
            self.time_elapsed = self.time.time()

        @staticmethod
        def primer_movimiento_detectado(self):
            print("Primer movimiento")

        @staticmethod
        def primer_preaviso_no_movimiento(self):
            print("Primer preaviso")

        @staticmethod
        def segundo_preaviso_no_movimiento(self):
            print("Segundo preaviso")

        @staticmethod
        def tercer_preaviso_no_movimiento(self):
            print("Tercer preaviso, por favor repita la instruccion")

        def mostrar_siguiente_video(self):
            tiempo = int(abs(self.time_elapsed - self.time.time()) * 100) / 100
            print("[main_move_detect]:", tiempo, ":", "Siguiente instruccion")
            dm.set_time(5)

            self.time_elapsed = self.time.time()

        @staticmethod
        def terminar_proceso(self):
            print("Proceso terminado")

    dm = Deteccion_movimiento(cam=0, clase=Proceso_deteccion_movimiento)

    time_elapsed = time.time()
    while True:
        frame = dm.get_frame()

        if not dm.hay_movimiento():
            if (int(abs(time_elapsed - time.time()) * 100) / 100) >= 10:
                time_elapsed = time.time()
                dm.iniciar_proceso_deteccion_movimiento()
        else:
            time_elapsed = time.time()

        cv2.imshow("frame", frame)

        time.sleep(0.025)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    dm.cerrar_camara()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main_move_detect()
