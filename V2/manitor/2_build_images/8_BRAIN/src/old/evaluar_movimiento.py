from urls import URL_MOVIMIENTO
from get import get


def evaluar_movimiento():
    movimiento = get(URL_MOVIMIENTO)

    if movimiento is not None:

        print("RTA:", movimiento)

        if 'move' in movimiento:
            movimiento = movimiento['move']
            return False if movimiento == 0 else True
        else:
            return False
    else:
        return False
