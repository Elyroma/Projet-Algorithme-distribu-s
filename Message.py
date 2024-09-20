class Message ():
    def __init__(self, message, time):
        self.message=message
        self.time=time

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message=message

    def getTime(self):
        return self.time
    
    def setTime(self, time):
        self.time=time

