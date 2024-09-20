from threading import Lock, Thread

from time import sleep

#from geeteventbus.subscriber import subscriber
#from geeteventbus.eventbus import eventbus
#from geeteventbus.event import event

#from EventBus import EventBus
from MessageWithTime import MessageWithTime
from BroadcastMessage import BroadcastMessage
from MessageTo import MessageTo
from TokenTP import Token
from Synchronize import Synchronizer

from pyeventbus3.pyeventbus3 import *

class Process(Thread):
    nbProcessCreated = 0
    def __init__(self, name, npProcess):
        Thread.__init__(self)

        self.npProcess = npProcess
        self.myId = Process.nbProcessCreated
        Process.nbProcessCreated +=1
        self.setName(name)
        self.horloge = 0
        self.token = None
        self.SC = False
        self.waitSynchronize = False
        self.synchronizer = None

        PyBus.Instance().register(self, self)

        self.alive = True
        self.start()

        if(self.myId == npProcess - 1):
            self.token = Token(self.myId, self.horloge)
        
    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageWithTime)
    def process(self, event):        
        print(self.getName() + ' Processes event: ' + event.getMessage())
        if(self.horloge < event.getTime()):
            self.horloge = event.getTime()
        self.horloge += 1

    @subscribe(threadMode = Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event):
        if(event.getSender() != self.myId):        
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.horloge < event.getTime()):
                self.horloge = event.getTime()
            self.horloge += 1
    
    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event):
        if(event.getReceiver() == self.myId):        
            print(self.getName() + ' Processes event: ' + event.getMessage())
            if(self.horloge < event.getTime()):
                self.horloge = event.getTime()
            self.horloge += 1
    
    @subscribe(threadMode = Mode.PARALLEL, onEvent=Token)
    def onToken(self, event):
        if(event.getReceiver() == self.myId):
            self.token = event    
            print(self.getName() + ' Processes event: Getting Token')
            if(self.horloge < event.getTime()):
                self.horloge = event.getTime()
            self.horloge += 1

    @subscribe(threadMode = Mode.PARALLEL, onEvent=Synchronizer)
    def onSynchronize(self, event):
        if(event.getSender() != self.myId):
            print(self.getName() + ' Processes event: Synchronized')
            if(self.horloge < event.getTime()):
                self.horloge = event.getTime()
            self.horloge += 1
            self.synchronize(event)


    def run(self):
        loop = 0
        while self.alive:
            print(self.getName() + " Loop: " + str(loop))
            sleep(1)

            if self.getName() == "P1":
                self.request()
                self.sendTo("Hey !", 0)
                self.release()
                self.requestSynchronized()

            if self.token != None and not self.SC:
                self.sendTokenToNext()

            if self.waitSynchronize:
                self.synchronizer.addSynchronizedProc()
                self.waitSynchronize = False
            

                while not self.synchronizer.allAreSynchronized():
                   time.sleep(1)
                self.synchronizer = None
                print(self.getName() + " Synchronized !")

            loop+=1
        
        
        print(self.getName() + " stopped")

    def stop(self):
        self.alive = False

    def waitStopped(self):
        self.join()

    def broadcast(self, o):
        self.horloge += 1
        message = BroadcastMessage(o, self.myId, self.horloge)
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)
    
    def sendTo(self, o, to):
        self.horloge += 1
        message = MessageTo(o, to, self.horloge)
        print(self.getName() + " send: " + str(message.getMessage()))
        PyBus.Instance().post(message)

    def request(self):
        print(self.getName() + " Request token")
        while(self.token == None):
            time.sleep(1)
        self.SC = True
    
    def release(self):
        #libère le token
        self.SC = False
        self.sendTokenToNext()

    def sendTokenToNext(self):
        self.horloge += 1
        receiver = (self.myId + 1) % Process.nbProcessCreated
        token = self.token
        token.setReceiver(receiver)
        token.setTime(self.horloge)
        print(self.getName() + " send: Token to " + str(token.getReceiver()))
        PyBus.Instance().post(token)
        self.token = None

    def synchronize(self, synchronizer):
        self.synchronizer = synchronizer
        self.waitSynchronize = True
        print(self.getName() + " Waiting synchronize")

    def requestSynchronized(self):
        self.horloge += 1
        request = Synchronizer(self.myId, Process.nbProcessCreated, self.horloge)
        print(self.getName() + " send: Synchronized request")
        PyBus.Instance().post(request)
        self.synchronize(request)