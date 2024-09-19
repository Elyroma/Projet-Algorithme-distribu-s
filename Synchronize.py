class Synchronizer ():
    def __init__(self, sender, nbProc, time):
        self.sender=sender
        self.nbProc=nbProc
        self.procSynchronized=0
        self.time=time

    def getSender(self):
        return self.sender

    def getTime(self):
        return self.time

    def getNbSynchronizedProc(self):
        return self.procSynchronized 

    def allAreSynchronized(self):
        return self.nbProc == self.procSynchronized

    def addSynchronizedProc(self):
        self.procSynchronized += 1