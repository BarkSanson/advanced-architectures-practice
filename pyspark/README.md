# Distributed systems: RDD with Pyspark

## Descripción
El objetivo de esta práctica es obtener, clasificado por edades, la
sesión de gimnasio más popular. Para ello, se utiliza Spark para procesar
los ficheros `session_Pilates.csv`, `session_yoga.csv`, `session_Spinning.csv` y
`user_age.csv`. En concreto, se utiliza Python con la librería de PySpark
para realizar el procesamiento de los datos.

## Despliegue de Spark
Para desplegar Spark, se han utilizado los ficheros contenidos en el
directorio `docker`. Para levantar el cluster, simplemente hará falta situarse
en este directorio y ejecutar
```shell
docker compose up
```
o
```shell
docker-compose up
```

## Funcionamiento
El código es muy sencillo y se encuentra únicamente en un archivo, `main.py`. El código
contenido en la función `main` de este fichero se podría dividir en seis partes:
1. Lee los archivos CSV y los convierte en RDDs.
2. Filtra los usuarios que sean menores de 18 y mayores de 60.
3. Por cada sesión, cuenta el número de veces que cada usuario ha asistido.
4. Junta cada una de las sesiones con el RDD de usuarios filtrados, agrupa
los usuarios por edad y suma el total de asistencias. 
5. Junta todos los RDDs por sesiones, comprueba cual de ellas tiene más
asistencias en cada edad y los ordena por edad.
6. Imprime por pantalla el resultado.

## Ejecución
Para ejecutar el código se necesitan realizar los siguientes pasos:
1. Levantar el cluster de Spark.
2. Copiar el directorio U9_data dentro del contenedor master de Spark. Es importante
guardar la ruta del directorio pues se necesitará para ejecutar el código. Esto
se puede hacer ejecutando
    ```shell
    docker cp U9_data <id-del-contenedor-master>:<ruta-en-el-contenedor>
    ```
3. Copiar el código de la práctica dentro del contenedor master de Spark. Esto
se puede hacer ejecutando.
    ```shell
    docker cp main.py <id-del-contenedor-master>:<ruta-en-el-contenedor>
    ```
4. Entrar en el contenedor ejecutando
    ```shell
    docker exec -it <id-del-contenedor-master> bash
    ```
5. Ejecutar `cd spark-3.5.0-bin-hadoop3`
6. Ejecutar
    ```shell
    ./bin/spark-submit --master local <ruta-fichero-main.py> <ruta-directorio-U9_data>
    ```