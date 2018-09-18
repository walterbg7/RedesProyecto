#Se abre la tabla para obtener los datos actuales solo en modo lectura
archivo = open("Tabla", "r")
linea = archivo.readlines()
archivo.close()

#Se abre la tabla en modo escritura para hacer cambios
archivo = open("Tabla", "w")
ip = input ("Digite la direccion de red: ")
costo = input("Digite el costo: ")
for i in linea:
    line = i.split("|")
    if ip == line[0]:
        if (costo < line[2]): #Si el costo de la nueva entrada es menor entonces se sobreescribe la linea
       	    i = line[0] +"|"+line[1]+"|"+ costo +"|"+line[3]  
    archivo.write(i)
archivo.close()

""" Tabla de alcazabilidad:
Direccion |  mascara | costo |  origen
192.168.0.0|16|5|10.1.4.55
192.166.0.0|16|4|10.1.4.55
192.167.0.0|16|3|10.1.4.55
"""
