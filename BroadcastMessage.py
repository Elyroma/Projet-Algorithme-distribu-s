from Message import Message
class BroadcastMessage (Message):
    def __init__(self, message, sender, time):
        Message.__init__(self, message, time)
        self.sender=sender

    def getSender(self):
        return self.sender