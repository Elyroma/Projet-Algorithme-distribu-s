class BroadcastMessage ():
    def __init__(self, message, sender, time):
        self.message=message
        self.sender=sender
        self.time=time

    def getMessage(self):
        return self.message

    def getSender(self):
        return self.sender

    def getTime(self):
        return self.time

