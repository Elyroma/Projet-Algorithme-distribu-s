from threading import Lock, Thread

from time import sleep
from BroadcastMessage import BroadcastMessage
from MessageTo import MessageTo

from pyeventbus3.pyeventbus3 import *

# Communicateur : envoi et réception de messages
# Contient une horloge de Lamport protégée par sémaphore

class Com ():
    def __init__(self, owner):
        self.owner=owner
        self.clock=0
        self.BaL=[]

    @subscribe(threadMode = Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        if(event.getSender() != self.owner.myId):    
            self.BaL.append(event.getMessage())    
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.clock < event.getTime()):
                self.update_clock(event.getTime())
            self.inc_clock()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event):
        if(event.getReceiver() == self.owner.myId):
            self.BaL.append(event.getMessage())
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.horloge < event.getTime()):
                self.update_clock(event.getTime())
            self.inc_clock()

    def update_clock(self, new_value): #idem
        self.clock = new_value

    def inc_clock(self): # Ajouter le sémaphore
        self.clock += 1

    def broadcast(self, o):
        self.inc_clock()
        message = BroadcastMessage(o, self.myId, self.clock)
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)

    def sendTo(self, o, dest):
        self.inc_clock()
        message = MessageTo(o, dest, self.clock)
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)        
