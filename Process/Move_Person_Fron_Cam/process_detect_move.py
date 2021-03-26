from DetectMoveSkinUtil import Deteccion_movimiento

if __name__ == "__main__":
    import cv2
    import time


    class Proceso_deteccion_movimiento:
        def iniciar_proceso(self):
            print("Proceso iniciado")

        def primer_movimiento_detectado(self):
            print("Primer movimiento")

        def terminar_proceso(self):
            print("Proceso terminado")

        def primer_preaviso_no_movimiento(self):
            print("Primer preaviso")

        def segundo_preaviso_no_movimiento(self):
            print("Segundo preaviso")

        def tercer_preaviso_no_movimiento(self):
            print("Tercer preaviso, por favor repita la instruccion")

        def mostrar_siguiente_video(self):
            print("Siguiente instruccion")
            dm.set_time(5)


    dm = Deteccion_movimiento(0, Proceso_deteccion_movimiento)

    chrono_temporal = dm.currentTime()
    while True:
        frame = dm.proceso_completo()

        if not dm.PROCESS_DETECT_MOVE:
            if abs(chrono_temporal - dm.currentTime()) >= 10:
                chrono_temporal = dm.currentTime()
                dm.iniciar_proceso_deteccion_movimiento()
        else:
            chrono_temporal = dm.currentTime()

        cv2.imshow("frame", frame)

        time.sleep(0.025)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    dm.cerrar_camara()
    cv2.destroyAllWindows()