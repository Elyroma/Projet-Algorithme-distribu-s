class Message ():
    def __init__(self, payload, stamp):
        """Contenu du message : payload
           Marque temporelle : stamp"""
        self.message=payload
        self.time=stamp

    def getPayload(self):
        return self.message

    def setPayload(self, message):
        self.message=message

    def getStamp(self):
        return self.time
    
    def setStamp(self, time):
        self.time=time

