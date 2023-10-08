# Distributed systems: networking
## Funcionamiento
Esta actividad consiste en un servidor de espera de jugadores, el cual, cuando
se llega a un número máximo de jugadores, el servidor espera cierto tiempo y se cierra.

El funcionamiento es muy sencillo: cuando el jugador se conecta, se le envía un mensaje
de bienvenida y se le informa a él y a los demás jugadores de la cantidad de jugadores
restantes. Además, cuando el jugadores se conecta también se informa a los demás jugadores.

## Uso
Para ejecutar esta práctica, simplemente se deberá encender el servidor con `python main.py`
y, desde la terminal, conectarse a él con `nc localhost 5000`. Si se desea cambiar el puerto,
se deberá hacer directamente desde el código modificando la constante `HOST`. De la misma
forma, si se desea cambiar el número máximo de jugadores, se podrá hacer cambiando la constante
`MAX_PLAYERS` contenida dentro de la clase `WaitHandler`.