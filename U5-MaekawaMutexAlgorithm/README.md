# Distributed Systems: Maekawa's Algorithm Voting System

## Introducción y funcionamiento
Esta práctica consiste en implementar el algoritmo de Maekawa. Este algoritmo es un algoritmo de exclusión
mutua distribuida que permite a un conjunto de procesos acceder a un recurso compartido de forma que se
garantice que no haya dos procesos accediendo al mismo tiempo al recurso. Para ello, se basa en la idea de
que los procesos se agrupan en subconjuntos de tamaño fijo llamados grupos de quórum. Este grupo debe ser
igual para todos los procesos, para garantizar igualdad. Además, la intersección de dos grupos de quórum
debe ser no vacía, para garantizar que siempre haya un camino hacia los demás nodos. 

En esta implementación, se simulan dos tiempos: el tiempo de reflexión del nodo y el tiempo de
ejecución de la sección crítica. Los nodos solo quieren acceder a la sección crítica una única vez.
Una vez que el nodo sale de la región crítica, simplemente espera a que los demás nodos entren y salgan
de esta. Una vez que todos los nodos han entrado y salido de la región crítica, el programa acaba.

## Mensajes
El formato del mensaje es el siguiente:
```python
{
    "msg_type": "Request" | "Reply" | "Release" | "Greeting",
    "src": int,
    "dest": int,
    "ts": int
}
```
Estos mensajes se envían en formato JSON entre los nodos. 

## Uso
Para ejecutar el programa, se debe ejecutar el siguiente comando:
```bash
python main.py
```