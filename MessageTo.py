class MessageTo ():
    def __init__(self, message, receiver, time):
        self.message=message
        self.receiver=receiver
        self.time=time

    def getMessage(self):
        return self.message

    def getReceiver(self):
        return self.receiver

    def getTime(self):
        return self.time

