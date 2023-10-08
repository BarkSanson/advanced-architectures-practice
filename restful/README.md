# Distributed system: a consensus group communication with Restful

## Funcionamiento
Esta práctica consiste en crear una arquitectura de consenso
basada en cliente-servidor haciendo uso de la librería Flask en Python. Esta
arquitectura consiste en un servidor y tres clientes/agentes. Cada agente
genera un número aleatorio (en esta implementación, un número aleatorio
del 1 al 10) y se lo envía al servidor. Si dos o más agentes han elegido el
mismo número, entonces hay consenso y los agentes finalizan. En caso contrario,
los agentes generan otro número aleatorio y siguen probando. 

## Endpoints

El servidor tiene dos *endpoints*:
- `/number`: 
  - Función: cada agente envía su número a este *endpoint* por medio
  de un JSON, el cual contiene un único campo `number` donde va el número
  generado por el agente.
  - Formato del JSON: `{ "number": <número_generado> }`
  - Método: `POST`.
- `/state/<id_client>`: 
  - Función: los agentes consultan este *endpoint* para saber el estado del servidor 
  (mirar siguiente sección), pasando su id por la URL.
  - Método: `GET`.

## Estados del servidor
El servidor puede estar en 3 estados:
- WAITING: el servidor está esperando a recibir los números generados por
todos los agentes.
- SUCCESS: el servidor ha recibido todos los números y ha habido mayoría.
- FAILED: el servidor ha recibido todos los números y no ha habido mayoría.

## Uso
Para ejecutar el servidor, simplemente se deberá introducir `python server.py`
en la terminal. Para inicializar los clientes, se deberá introducir `python client.py <id>`
en la terminal. Ejemplo: `python client.py 1`.

**Nota**: el servidor se deberá ejecutar **siempre** antes que cada cliente.

**Nota 2**: el id de cada cliente deberá ser diferente al de los demás. Si se
introduce el mismo id para dos o más clientes, el servidor los confundirá y
no podrá realizar correctamente sus funciones.

## ¿Este método es adecuado para establecer una comunicación de grupos?
La arquitectura cliente-servidor, implementada de esta forma, tiene más
desventajas que ventajas. La ventaja principal es que se centraliza la
lógica "de negocio" en un mismo punto. Es decir, la función de comprobar
la mayoría se hace desde el servidor, y este simplemente informa a cada
agente del resultado. Sin embargo, esto se traduce en una alta carga (en
casos de uso más complejos) de trabajo sobre el servidor, ya que debe
gestionar las peticiones de todos los agentes. Además, el servidor se convierte
en un punto único de fallos. Por tanto, la caída del servidor se traduce
en un fallo total del sistema. Esto contrasta con un consenso distribuído,
donde, si un nodo falla, se traduce en un fallo parcial del sistema.
