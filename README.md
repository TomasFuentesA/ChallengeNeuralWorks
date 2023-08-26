# ChallengeNeuralWorks
Challenge de NeuralWorks

## Tabla de contenidos

- [Supuestos](#Supuestos)
- [Ejecución](#Ejecucion)
- [Situaciones de Mejora](#Situaciones_de_Mejoras)
- [Escalabilidad](#Escalabilidad)
- [GCP](#GCP)
- [License](#license)

## Supuestos
- En primer lugar, el CSV otorgado fue considerado como una fuente de stream de datos, la idea era poder emular un "caso real" en donde los datos llegan en tiempo real.
- Segundo, las respuestas a los problemas se consideraron como funcionas que retornan los solicitado. Se toma este metodo pensando en la idea de que son servicios que se pueden requerir en cualquier momento.
- Tercero, la creación del "topic" de kafka se hace de manera manual en la consola de docker y con el nombre "test", debido a que es un entorno de pruebas de este caso.
- El dato POINT, se guardan por separado en la BD para hacer más fácil su manejo.

## Ejecución
- Primero, para ejecutar la solución se deben correr los siguientes comandos:
```shell
$ docker-compose up -d
```
- Una vez iniciado, se debe ir al CLI de Kafka en Docker y usar el siguiente comando para crear el topic a usar.
```shell
$ kafka-topics.sh --create --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --topic test
```
- Luego de la creacion del topic iremos a la CLI del consumer y del producer respectivamente y usaremos lo siguiente:
```shell
$ python consumer.py
$ python producer.py
```
- Estos comandos haran que se inicien nuestro producer y consumer de kafka. El producer emulara una emisión de los datos del csv y el consumer, los recibira y los almacenara en la base de datos. Cabe destacar que el consumer ademas de recibir los datos (los cuales se mostraran por consola), tambien mostrará el estado en que se encuentra la ingesta de datos, por ejemplo iniciado, finalizado y cancelado.
- Finalmente, los funcionalidades solicitadas se encuentran encapsuladas como funciones para que puedan ser utilizadas y llamadas desde otros lugares (pensando en un caso a mayor escala)
- Para el primer problema vamos a ir al CLI del contenedor de problema 1 y usar el siguiente comando:
```shell
$ python agrupar_similares.py
```
- Lo que hara esta archivo es ejecutar el script que usara en algoritmo de clustering para poder agrupar viajes parecidos y añadir al cluster que pertenecen a la base de datos e imprimir por pantalla esos clústers.
- Y por último, iremos a la CLI del contenedor del problema 2 y ejecutaremos lo siguiente:
```shell
$ python
$ import promedio_semanal
$ agrupar_similares.get_weekly_mean(region, lat_origin, long_origin, lat_destination, long_destination)
```
- De esta forma se podra calcular el promedio semanal de todos los viajes que se encuentran dentro del bounding box y region escogidas (No esta de más recorda que los argumentos deben ser los que desees probar, ej: promedio_semanal.get_weekly_average('Turin',7,45,8,46))
- Y para bajar todo debe usar lo siguiente en la consola que uso para levantar todo:
```shell
$ docker-compose down
```
## Situaciones de mejora
- La primera gran mejora que se puede añadir al sistema, es acompañar el informe de control en la ingesta de datos con acciones como, guardar logs del timestamp en comenzo y en el que finalizó. Como así tambien guardar logs de las interrumpciones ocurridas en el sistema.
- Agregar nuevas posibles interrupciones, en mi caso escogi la tipica el KeyInterrupt, pero en un caso real, podemos encontrar muchas más situaciones en las que se puede ver afectada (y de mala manera) la ingesta de datos. Por ejemplo excepciones de entrada y salida donde existen cierres inesperados de sockets o puertos.
- Acompañado de esto, es importante añadir sistemas de recuperación en caso de cortes o interrupciones. Guardar checkpoints de manera periodica, permite mantener el sistema listo en caso de emergencia.
- Por otro lado, como mejora podria ser la utilización de bases de datos no relacionales en conjunto de las relacionales, es posible mientras se reciba mucha data de distintos lugares alguna sea no estructurada por ende sería necesaria la utilizacion de un BD no estrucutral.
- Usar otro tipo de herramientas distribuida como Spark por ejemplo, que nos ayudaria en el caso de agrupar grandes volumenes de datos con sus librerias de ML y además de otorgar escalibilidad, otorga eficiencia y rendimiento.
## Escalabilidad
- La escalabilidad esta presente en dos grandes protagonistas Kafka y Docker. Partiendo por kafka, al tener muchos datos, del orden de millones este nos permite replicar nuestros producers y consumers, para asi poder dar abasto a la cantidad de demanda del sistema. También es posible manejar clústers con múltiples nodos para mantener la redundancia y asi garantizar la no perdida de los datos y los distintos servicios sigan funcionando sin problemas.
- Por otro lado el uso de contenedores, nos permite replicar servicios y no sobrecargar uno en especifico, de esta forma podemos mantener muchos contenedores identicos procesando datos sin sobrecargar alguno y en caso de que alguno falle, se utiliza algún balanceador de carga para poder repartir las tareas que deban finalizarse y que el contenedor que fallo no pueda realizar.
- Creo que la situación de mejora más notoria es automatizar todo (o la gran mayoria) y tratar de minimizar el añadir comandos manualmente.
  
## GCP
- Para montar todo en GCP, considero que deben haber 4 puntos claves:
- Kubernetes permitirá manejar clústers de herramientas distribuidas que podrán capturar la data en tiempo real que llegue al sistema.
- Luego viene Dataflow, el cual nos permitirá preprocesar todas nuestra data para los estudios que sea necesarios.
- BigQuery será nuestro almacen, alli guardaremos toda nuestra data preprocesada que será útil para alimentar modelos de ML o realizar análisis de estos datos.
- Cloud Endpoints, nos permitira manejar nuestros servicios, los cuales realizaran consultas a BigQuery para obtener los datos necesarios según su funcionalidad.
  
<p align="center">
  <img src="https://github.com/TomasFuentesA/ChallengeNeuralWorks/assets/69986261/8c6b7e24-8f40-4af5-abe4-7acc2d8e84be" alt="DiagramaGCP">
</p>
