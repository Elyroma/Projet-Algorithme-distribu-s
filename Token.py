from time import sleep
from threading import Thread

class Token ():
    def __init__(self, receiver):
        self.receiver=receiver
        
    def getReceiver(self):
        return self.receiver

    def setReceiver(self, receiver):
        self.receiver=receiver


class TokenManager(Thread):
    def __init__(self, com):
        Thread.__init__(self)
        self.com = com
        self.alive = True
        self.start()

    def run(self):
        while self.alive:
            if self.com.token is not None and not self.com.SCRequestSend:
                self.com.sendTokenToNext()
                time.sleep(1) 

    def waitStopped(self):
        self.join()

    def stop(self):
        self.alive = False
        self.join()