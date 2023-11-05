# Distributed systems: an indirect group communication using MQTT

## Descripción
Esta práctica consiste en la implementación del juego Tres en Raya
(*tic-tac-toe*, en inglés) en un sistema distribuido. Para esto, se deben
implementar dos agentes que se comunican entre sí mediante el protocolo MQTT.

## Implementación
En esta implementación, los dos agentes son exactamente iguales, diferenciándose
únicamente en el tipo de pieza que juegan: círculo o cruz. 
Como *broker* MQTT se ha utilizado Eclipse Mosquitto, desplegado en un contenedor de 
Docker. Los agentes se han implementado en Python, utilizando la librería paho-mqtt.

Los mensajes que se intercambian los agentes son muy sencilos, y tienen la siguiente
estructura JSON:
```
{
    "player": <"X" | "O">,
    "row": <0 | 1 | 2>,
    "col": <0 | 1 | 2>
}
```
Estos mensajes se envían al *topic* "tic-tac-toe".

## Ejecución
Para ejecutar el juego, se debe ejecutar el comando
```bash
python main.py <player>
```

Donde `<player>` es el tipo de pieza que juega el agente: "X" o "O". Para
evitar problemas de sincronización, se recomienda ejecutar primero el
agente X y después el agente O. Hay un margen de 5 segundos antes de que el
agente inicie la comunicación.
