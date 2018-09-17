from threading import Thread
from random import randint
import time
class MyThread(Thread):
	def __init__(self, val):
		''' Constructor. '''
		Thread.__init__(self)
		self.val = val
 
 
	def run(self):
		for i in range(1, self.val):
             		print('Value %d in thread %s' % (i, self.getName()))
 
             		# Sleep for random time between 1 ~ 3 second
             		secondsToSleep = randint(1, 5)
             		print('%s sleeping fo %d seconds...' % (self.getName(), secondsToSleep))
             		time.sleep(secondsToSleep)
 
class serverUDP(MyThread):
	def __init__(self, n):
		MyThread.__init__(self, 5)

	def ptable(self):
		while(1):
			print("tabla de alca")
			time.sleep(5)

	def run(self):
			serverT = Thread(target=self.ptable, args=())
			serverT.start()
			print("paralalala")

 
# Run following code when the program starts
if __name__ == '__main__':
   # Declare objects of MyThread class
	myThreadOb1 = serverUDP(4)
	myThreadOb1.setName('Thread 1')

	myThreadOb2 = serverUDP(5)
	myThreadOb2.setName('Thread 2')

	# Start running the threads!
	myThreadOb1.start()
	myThreadOb2.start()

	# Wait for the threads to finish...
	myThreadOb1.join()
	myThreadOb2.join()
	 
	print('Main Terminating...')	
