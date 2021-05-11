BRAIN:
1- pregunta cada 5 segundos a 4)[http://localhost:5004/name] el cercano
   1.1. nuevo nombre: active bandera
   1.2. no hay mas procesos
2- valida que el actual es el mismo anterior (si es diferente => envia por 7) el vector)
3- cada 100msg verifico primer movimiento con 6) {'move':1,'acc':%%}
    3.1. si no hay movimiento luego de 5 segundos, anule la bandera y reinicie el proceso
4- inicio lavado manos (contabilizar primer movimiento)
5- activo sonido por 2) [http://localhost:5002/reproduce?id=1] y activo video 5) [http://localhost:5005/mostrar?id=3&name=WilliamRodriguez]
5- cada 100msg consulto a 6) {'move':1,'acc':%%}
    5.1. No hay movimiento: activo el 5) [http://localhost:5005/mostrar?id=3&name=WilliamRodriguez] con penalidad (con 3 penalidades invoco a 7)
    5.2. si hay movimiento, cuento tiempo para final de paso e indico nuevo paso por 2), 5) y 7)
6- si no hay mas pasos, invoco a 7)