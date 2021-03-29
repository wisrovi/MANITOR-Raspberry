TIEMPO_POR_INSTRUCCION = 15
TIEMPO_AVISO_NO_MOVIMIENTO = 10
TIEMPO_DESCANSO_ENTRE_UNA_PERSONA_Y_OTRA_CUANDO_LA_PRIMERA_COMPLETO_DESINFECCION = 35

constante_cambio_area = 1000  # constante de cambio de area, entre mayor sea el numero, mayor es el area a detectar para cambio, es decir el equivalente a la velocidad de movimiento
valor_cambio = 200  # Constante incremental para cambio de estado [Lavandose_manos, Persona_ausente_o_sin_movimiento]

STATUS_MOVIMIENTO = ("MOVE", "NO_MOVE")

TIEMPO_VOLVER_LAVAR_MANOS = 60  # segundos (recomendado 5 minutos)

FILE_MOVE_DETECT = "json_move_detect.json"

