import pika

class Process:
    def __init__(self, id):
        self.id = id
        self.is_initiator = False
        self.state = id * 3 # mb bank balance
        self.__state_storage = 0
        self.neighbors = []
        self.get_connection()

    def record_state(self):
        self.__state_storage = self.state
    
    def show_snapshot_state(self):
        return self.__state_storage

    def get_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    
    def close_connection(self):
        self.connection.close()

    def broadcast_marker(self):
        pass