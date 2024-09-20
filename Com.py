from threading import Lock, Thread

from time import sleep
from BroadcastMessage import BroadcastMessage
from MessageTo import MessageTo
from Token import Token, TokenManager

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
        
        
        self.token = None
        self.SCRequestSend = False
        if(self.myId == 0):
            self.token = Token(self.getMyId())
        self.tokenManager = TokenManager(self)

            #time.sleep(1)
            #token = Token(0)
            #PyBus.Instance().post(token)
            #Thread(target=send_initial_token, args=(self,)).start()
    

    def __del__(self):
        self.tokenManager.stop()
        self.tokenManager.waitStopped()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        
        if(event.getSender() != self.getMyId()):    
            self.BaL.append(event.getPayload())    
            print(self.getName() + ' Processes event: ' + event.getPayload())
            if(self.getClock() < event.getStamp()):
                self.updateClock(event.getStamp() + 1)
            else :
                self.incClock()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event):
        if(event.getReceiver() == self.getMyId()):
            self.BaL.append(event.getPayload())
            print(self.getName() + ' Processes event: ' + event.getPayload())
            if(self.getClock() < event.getStamp()):
                self.updateClock(event.getStamp() + 1)
            else :
                self.incClock()

    @subscribe(threadMode = Mode.PARALLEL, onEvent=Token)
    def onToken(self, event):
        if(event.getReceiver() == self.getMyId()):
            self.token = event    
            print(self.getName() + ' Processes event: Getting Token')
            #time.sleep(1)
            #if not self.SCRequestSend:
            #    self.sendTokenToNext()

    def updateClock(self, new_value):
        """Met à jour l'horloge avec une nouvelle valeur."""
        with self.clock_available:
            self.clock = new_value

    def incClock(self):
        """Incrémente l'horloge."""
        with self.clock_available:
            self.clock += 1

    def getClock(self):
        """Récupère la valeur de l'horloge."""
        with self.clock_available:
            return self.clock

    def broadcast(self, o):
        self.incClock()
        message = BroadcastMessage(o, self.getMyId(), self.getClock())
        print(self.getName() + " send: " + str(message.getPayload()))
        PyBus.Instance().post(message)

    def sendTo(self, o, dest):
        self.incClock()
        message = MessageTo(o, dest, self.getClock())
        print(self.getName() + " send: " + str(message.getPayload()))
        PyBus.Instance().post(message)

    def requestSC(self):
        """Demande la section critique."""
        print(self.getName() + " Request token")
        self.SCRequestSend = True
        while(self.token == None):
           time.sleep(1)
    
    def releaseSC(self):
        """Libère la section critique."""
        self.SCRequestSend = False
        #self.sendTokenToNext()

    def sendTokenToNext(self):
        if self.token is not None:
            receiver = (self.myId + 1) % Com.nbProcessCreated
            token = self.token
            token.setReceiver(receiver)
            print(self.getName() + " send: Token to " + str(token.getReceiver()))
            PyBus.Instance().post(token)
            self.token = None  
        else :
            print("Error: No token to send")

    def getNbProcess(self):
        return Com.nbProcessCreated   

    def getMyId(self):
        return self.myId
    
    def getName(self):
        return "C" + str(self.myId)
