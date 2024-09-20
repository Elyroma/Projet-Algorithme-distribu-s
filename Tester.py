from threading import Lock, Thread

from time import sleep

from Com import Com

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    
    def __init__(self,name):
        Thread.__init__(self)

        self.com = Com()
        PyBus.Instance().register(self.com, self)
        
        self.nbProcess = self.com.getNbProcess()

        self.myId = self.com.getMyId()
        self.setName(name)


        self.alive = True
        self.start()
    

    def run(self):
        loop = 0
        print(self.getName() + " " + self.com.getName())
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P0":
                self.com.broadcast("il y a quelqu'un ?")
                self.com.sendTo("j'appelle 2 et je te recontacte après", 1)
                print(self.getName() +" horloge test : " + str(self.com.getClock()))
                

            loop+=1
        print(self.getName() + " stopped")

    def waitStopped(self):
        self.join()

    def stop(self):
        self.alive = False
        self.join()
