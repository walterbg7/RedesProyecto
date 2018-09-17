from threading import Thread
from socket import *

class Server(Thread):
	def __init__(self, ip, mask, port):
		Thread.__init__(self)
		self.ip_address = ip
		self.mask = mask
		self.port = port
		# Falta tabla de alcanzabilidad
 
class Server_UDP(Server):
	def listen(self):
		serverSocket = socket(AF_INET, SOCK_DGRAM)
		serverSocket.bind((server.ip_address, self.port))
		print ("The server is ready to receive")
		while (1):
			message, clientAddress = serverSocket.recvfrom(2048)
			print(str(clientAddress))
			print(str(message))
			modifiedMessage = message.upper()
			serverSocket.sendto(modifiedMessage, clientAddress)

class Server_TCP(Server):
	def listen(self):
		serverSocket = socket(AF_INET, SOCK_STREAM)
		serverSocket.bind((server.ip_address, self.port))
		serverSocket.listen(1)
		print ("The server is ready to receive")
		while (1):
			connectionSocket, addr = serverSocket.accept()
			sentence = connectionSocket.recv(1024)
			print (str(addr))
			print (str(sentence))
			capitalizedSentence = sentence.upper()
			connectionSocket.send(capitalizedSentence)
			connectionSocket.close()


class Client:
	def __init__(self):
		# Constructor
		# Tabla de alcanzabilidad
		print("Constructor :)")

	def print_table(self):
		# Imprimir tabla de alcanzabilidad
		print("Tabla :)")
 
class Client_UDP(Client):
	def send(self):
		#Enviar Mensaje
		print("Mensaje :)")

class Client_TCP(Client):
	def __init__(self):
		# Constructor
		# Tabla de alcanzabilidad
		# Lista de conexiones
		print("Constructor :)")


# Run following code when the program starts
if __name__ == '__main__':

	server = Server_UDP("", 0, 12000)
	server.setName('Thread 1')

	server.start()
	server.listen()
	 
	print('Main Terminating...')	
