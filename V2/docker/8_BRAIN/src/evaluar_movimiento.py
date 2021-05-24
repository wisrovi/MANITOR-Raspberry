from urls import URL_MOVIMIENTO
from get import get


def evaluar_movimiento():
    movimiento = get(URL_MOVIMIENTO)
    # COMENTAR CUANDO SE CONFIGURE LA URL
    # movimiento = '{ "acc": 57, "time": "11/5/2021-17:24:47", "move": 1 }'
    # movimiento = json.loads(movimiento)

    if movimiento is not None:

        print("RTA:", movimiento)

        if 'move' in movimiento:
            movimiento = movimiento['move']
            return False if movimiento == 0 else True
        else:
            return False
    else:
        return False
