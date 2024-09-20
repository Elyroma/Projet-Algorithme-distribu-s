from threading import Lock, Thread

from time import sleep
from BroadcastMessage import BroadcastMessage
from MessageTo import MessageTo

from pyeventbus3.pyeventbus3 import *

# Communicateur : envoi et réception de messages
# Contient une horloge de Lamport protégée par sémaphore

class Com ():
    nbProcessCreated = 0
    def __init__(self):
        self.myId = Com.nbProcessCreated
        Com.nbProcessCreated +=1

        self.clock=0
        self.clock_available = Lock()
        self.BaL=[]

    @subscribe(threadMode = Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        if(event.getSender() != self.getMyId()):    
            self.BaL.append(event.getMessage())    
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.clock < event.getTime()):
                self.update_clock(event.getTime() + 1)
            else :
                self.inc_clock()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event):
        if(event.getReceiver() == self.getMyId()):
            self.BaL.append(event.getMessage())
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.horloge < event.getTime()):
                self.update_clock(event.getTime() + 1)
            else :
                self.inc_clock()

    def update_clock(self, new_value):
        """Met à jour l'horloge avec une nouvelle valeur."""
        with self.clock_available:
            self.clock = new_value

    def inc_clock(self):
        """Incrémente l'horloge."""
        with self.clock_available:
            self.clock += 1

    def get_clock(self):
        """Récupère la valeur de l'horloge."""
        with self.clock_available:
            return self.clock

    def broadcast(self, o):
        self.inc_clock()
        message = BroadcastMessage(o, self.getMyId(), self.get_clock())
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)

    def sendTo(self, o, dest):
        self.inc_clock()
        message = MessageTo(o, dest, self.get_clock())
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)  

    def getNbProcess(self):
        return Com.nbProcessCreated   

    def getMyId(self):
        return self.myId
    
    def getName(self):
        return "C" + str(self.myId)
