# Programación paralela: implementación de tres algoritmos de ordenación con paralelismo

## Introducción
Los algoritmos de ordenación conforman una parte importante de la base de las ciencias de la computación. Estos son aplicables para infinidad de tareas: ordenación de registros en bases de datos, ordenación de cadenas de texto, procesamiento de imágenes, etc. Cada uno de los algoritmos utiliza técnicas distintas de ordenación. Muchos se basan en la ordenación parcial de los datos para finalizar con la ordenación total. Por ejemplo, el Quicksort ordena parcialmente los elementos en función de si son mayores o menores que un pivote. Con estas ordenaciones parciales, después de algunas iteraciones, se consigue que el vector esté totalmente ordenado.

Las formas clásicas tienen forma secuencial. Sin embargo, al no existir dependencias entre datos en muchas de las operaciones que se realizan para la ordenación, estas se pueden realizar en paralelo. Siguiendo con el ejemplo del Quicksort, comprobar si un elemento es mayor o menor que otro es independiente de los demás elementos del vector y, por tanto, paralelizable. 

Esta práctica consiste en la implementación de Mergesort, QuickSort y Radixsort utilizando la librería Intel Threading Building Blocks, la cual permite la paralelización de operaciones de forma sencilla y abstrayendo al programador del trabajo con hilos y sincronización.

## Paralelismo en las implementaciones de este proyecto
Empezando por el Mergesort, el paralelismo se encuentra en dos puntos principalmente. En primer lugar, se convierten cada uno de los elementos del vector a un vector que contenga ese elemento. Esto se puede implementar fácilmente de forma paralela, pues no existe ninguna dependencia de datos, con `parallel_for`. El segundo punto es el de fusionar cada uno de los vectores de forma ordenada. Si se fusionan dos vectores, sí que es necesario que sea de forma secuencial. Sin embargo, se puede hacer esta fusión dos a dos de forma paralela con `parallel_reduce`, pues no existe ninguna dependencia entre los dos vectores a fusionar y otro vector de la lista. La implementación realizada en este proyecto está basada en la diapositiva 121 "Merge Sort as a scan: Tree Shape". 

Siguiendo con el Quicksort, el paralelismo se encuentra en tres partes. En primer lugar, en las llamadas recursivas a Quicksort. Al estar modificando cada una de las llamadas partes distintas del vector, se pueden ejecutar en paralelo con `parallel_invoke`. A continuación, en la comprobación de si un elemento es menor que el pivote. Como se ha mencionado antes, esta comprobación no tiene ninguna dependencia, así que se puede realizar en paralelo con `parallel_for`. Finalmente, existe paralelismo en la creación de los índices de cada uno de los elementos, y se ha implementado con `parallel_scan`.

Por último, el Radixsort tiene principalmente dos puntos de paralelismo, y son en la creación de los índices de los números con el bit $i$ a 0 o a 1, ambos implementados con `parallel_scan`.

## Aclaraciones
En este proyecto se incluyen todos los ficheros `.hpp` y `.cpp` con el nombre de cada uno de los algoritmos. Además, hay dos propuestas que mejoran el paralelismo de Quicksort y Radixsort. Estos ficheros son los que tienen nombre `quickSort_proposal` y `radixSort_proporsal`. Estos ficheros son los ideales en cuanto a paralelismo, pero que generan _segmentation faults_ por alguna razón que no se ha podido descubrir.

Por un lado, `quickSort_proposal` cambia la implementación de `quickSort`. En esta implementación, se añaden las funciones `gather_if`, `get_smaller_equal` y `get_greater`. En las dos últimas funciones se comprueban los números que son menores o iguales o mayores que el pivote, respectivamente, utilizando `parallel_for`. Ambas llaman a `gather_if`, la cual genera los respectivos índices con `parallel_scan`. Esta implementación devuelve un vector y no modifica el pasado por parámetro, a diferencia de `quickSort`.

Por otro lado, `radixSort_proposal` añade paralelismo a la hora de mapear los números al bit $i$, y al reordenar el vector con los índices, todo con `parallel_for`.

Al no poder descubrir por qué se generan los _segmentation faults_, se ha reducido el paralelismo tanto en Radixsort y Quicksort, cuyas versiones finales se encuentran en los archivos con nombre `radixSort` y `quickSort`, respectivamente. De cualquier forma, se añaden estas propuestas como observación de que es posible añadir más paralelismo a los algoritmos.

## Uso
Este proyecto contiene un fichero `main.cpp`, el cual se ha utilizado para realizar las pruebas. Estas pruebas han consistido en generar un vector aleatorio, cambiando su tamaño entre pruebas, utilizar cada uno de los algoritmos y comprobar si el resultado de cada uno de los algoritmos es correcto.

Si se quiere utilizar este fichero `main.cpp`, se puede ejecutar `bazel run //:SortAlgorithms` en la raíz del proyecto. Los resultados se mostrarán por consola.

Si se quieren utilizar los algoritmos como librería, será necesario incluir el _header_ de cada uno de los algoritmos y modificar los archivos de configuración del sistema de compilación que se esté utilizando.

Es importante destacar que tanto Mergesort como Radixsort devuelven un vector ordenado, sin modificar el vector original, a diferencia de Quicksort que sí lo modifica. Por tanto, a la hora de utilizar Quicksort se recomienda pasarle por parámetro una copia del vector original, si se desea inmutabilidad en este último.

## Pruebas
Las pruebas, como se ha dicho antes, han consistido en la comprobación de que los vectores generados aleatoriamente estén correctamente ordenados. En total, se han realizado 20 ejecuciones, todas dando un resultado positivo.