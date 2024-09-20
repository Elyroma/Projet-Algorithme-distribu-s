class Token ():
    def __init__(self, receiver, time):
        self.receiver=receiver
        self.time=time

    def getReceiver(self):
        return self.receiver

    def getTime(self):
        return self.time

    def setReceiver(self, receiver):
        self.receiver=receiver

    def setTime(self, time):
        self.time=time