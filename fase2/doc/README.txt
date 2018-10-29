Manual de ususario:
Para probar la implementación de la clase PseudoTCP se brindan dos codigos de prueba (uno para el servidor y otro para el receptor).
1- Primero se recomienda ejecutar el codigo de prueba del servidor (pseudoTCPServerTest.py) con el siguiente comando:
    $ python3 pseudoTCPServerTest.py

Este codigo le va a solicitar un numero de puerto al cual va escuchar el servidor (recuerde que el rango de puertos validos es ]0, 65536[, se recomienda usar un puerto no reservado, es decir mayor a 1023).
2- Segundo se debe correr el codigo de prueba del cliente (pseudoTCPClientTest.py) con el siguiente comando:
    $ python3 pseudoTCPClientTest.py

Este programa le va a pedir la dirección IP y el número de puerto del servidor al que se desea conectar (se deben brindar los datos basandose en la maquina donde se ejecuto el codigo pseudoTCPServerTest.py).
Ademas le va a solicitar la ruta del archivo de texto que se desea enviar, para este ejecto se adjunta en la carpeta "test" del entregable, el documento de texto test0.txt con la letra de una canción, no obstante se puede pasar cualquier archivo de texto plano.

3- Finalmente se debe ver en la carpeta del lado servidor, donde se ejecutó el codigo pseudoTCPServerTest.py, un archivo llamado "recivedFile.txt" con el contenido del archivo enviado por el ultimo cliente.
