class Token ():
    def __init__(self, receiver):
        self.receiver=receiver
        
    def getReceiver(self):
        return self.receiver

    def setReceiver(self, receiver):
        self.receiver=receiver