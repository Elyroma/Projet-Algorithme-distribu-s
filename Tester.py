from threading import Lock, Thread

from time import sleep

from Com import Com

class Process(Thread):
    
    def __init__(self,name):
        Thread.__init__(self)

        self.com = Com()
        
        self.nbProcess = self.com.getNbProcess()

        self.myId = self.com.getMyId()
        self.setName(name)


        self.alive = True
        self.start()
    

    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P0":
                self.com.sendTo("j'appelle 2 et je te recontacte après", 1)
                print(self.getName() +" horloge test : " + str(self.com.get_clock()))
                

            loop+=1
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False
        self.join()
