from Message import Message
class MessageTo (Message):
    def __init__(self, message, receiver, time):
        Message.__init__(self, message, time)
        self.receiver=receiver

    def getReceiver(self):
        return self.receiver
