GetConf
=======
Getconf (Version CGR) 1.7 Aplicacion Multihilo escrita en Python para realizar una copia de seguridad de todos los 
routers (Cisco y Teldat) gestionados por el CGP en remoto de una forma rápida y sencilla.

Este documento describe el procedimiento para realizar una copia de seguridad de todos los routers (Cisco y Teldat)
gestionados por el CGP de una forma rápida y sencilla.
Getconf 1.7 realiza las siguientes acciones de forma automática:
-    Accede a los equipos (Cisco y Teldat).
-	Ejecuta la orden “show running-config”.
-	Captura la salida del terminal.
-	Guarda el resultado en archivos de texto.
-	Los archivos son agrupados por LOTE en carpetas distintas.

La aplicación Getconf 1.7 nos permite guardar la configuración de un numero ilimitado de routers en poco tiempo de
una forma rápida y eficiente.
Para que la aplicación se ejecute correctamente requiere tener instalado el interprete de Python versión 2.5
o superior, (la próxima versión sera compilada para ejecutarla en cualquier equipo sin necesidad de interprete).

Getconf usa un archivo de texto para leer las direcciones IP de los equipos a los que queremos hacer la copia 
de seguridad, el archivo de texto debe estar en la carpeta raíz del programa llamándose “list_ip.txt” dentro del 
documento las IP’s deben estar en una sola columna alineadas a la izquierda, (como se muestra en el ejemplo).

Para el optimo funcionamiento del programa es aconsejable copiar la carpeta del programa (de Servicios_TIC) a una 
carpeta en nuestro equipo en LOCAL (ejem: C:\) y ejecutarlo desde ahí.
Importante: Es necesario tener instalado Python versión 2.5 o superior para ejecutar correctamente la aplicación.
Al ejecutar Getconf nos pide usuario y contraseña, cada operador debe introducir su propio TACACS personal para acceder
a los equipos Cisco. Importante: Revisar que el TACACS introducido es correcto ya que Getconf no valida y si es 
incorrecto provocara error de acceso a los equipos (el cual será registrado en el LOG). Después de introducir USERNAME
y  PASSWORD correctos, Getconf nos pedirá un nombre para el archivo “LOG” de registro. 

En el archivo LOG se irán registrando todos los eventos generados por la tarea, guarda la hora de inicio y fin de la
tarea, si hay algún error también será registrado, de tal modo que al terminar el programa podemos saber cuales 
equipos no han respondido por estar apagados o en incidencia (error de acceso, incomunicación, perdida de gestión, etc…).

Una vez que se haya creado el archivo LOG Getconf comenzara a realizar la copia de seguridad en los routers indicados 
(se puede modificar el numero de conexiones simultaneas para optimizar el trabajo en función a la capacidad de la red),
la salida en pantalla se ira actualizando en tiempo real. Automáticamente captura las salidas del comando
“show running-config” que ejecuta  en cada router y las ira guardando dentro de la carpeta "/Getconf/bckp_files” 
utilizando como nombre para los archivos la fecha y el nemónico de TDE. Para abortar la ejecución del programa en 
cualquier momento se puede hacer pulsando Control+C, Una vez finalizado el proceso, Getconf preguntara si desea 
visualizar un listado con todas las IP’s que han provocado un error, (también se puede ver desde el archivo LOG). 
Con el listado sabemos que equipos han dado error y es posible volver a ejecutar la tarea sobre esas IP’s.

Una vez se haya completado la tarea, copiaremos los nuevos archivos en
S:\Servicios_TIC\CGR\carpeta Q\COPIA DE LINUX\Copias de respaldo - PLANTA\Respaldo_por_fechas”, dentro de una carpeta
creada por nosotros con el siguiente formato “Respaldo_año-mes-dia”. Posteriormente enviar una notificación por 
correo al CGR (cgr@salud.madrid.org), indicando que la copia de respaldo se ha realizado con éxito.

Se pueden modificar algunos parámetros de Getconf para optimizar su funcionamiento, los cambios se pueden realizar 
directamente en el código del programa.
-	thread_multi = 50
-	Getconf tiene soporte multithreading (multihilo), es el numero de hilos simultáneos permitidos. Por defecto 50. 
(Esto afecta a la cantidad de conexiones simultaneas). 
-	thread_time_out = 0.25 
Es el tiempo de espera en mili-segundos entre hilos. (Para no saturar con el disparo de hilos).
-	enable_pass = 's0!0c0re\n' 
Es la clave de acceso en modo privilegiado de CISCO. (En este caso es s0!0c0re, la “\n” sirve para enviar un retorno
de carro (Entrar) al terminal.
-	Todos los métodos “time.sleep()” dentro de la función Save_cisco() son tiempos de  espera para capturar los datos
que recibimos desde los equipos remotos, cada LOTE tiene un retardo distinto. (Por ejemplo un acceso ADSL es mas 
lento que acceso MACROLAN de FIBRA) Con esto conseguimos mayor velocidad en el procedimiento y garantiza que 
recibimos la salida completa del la orden “show running-config”.




