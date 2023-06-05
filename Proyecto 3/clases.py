class Client:
    def __init__(self, id_client):
        self.id_client = id_client

class Event:
    def __init__(self, id_client, tipe, time):
        self.id_client = id_client
        self.tipe = tipe
        self.time = time
        

class Queue:
    def __init__(self, id_queue):
        self.id_queue = id_queue
        self.clients = []
        self.server = False