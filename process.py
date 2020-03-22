import pika

class Process:
    def __init__(self, id):
        self.id = id
        self.is_initiator = False
        self.is_marked = False
        self.states = []
        self.__state_storage = []
        self.__message_storage = []
        self.neighbors = []
        self.get_connection()

    def get_connection(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()

    def close_connection(self):
        self.channel.close()
        self.connection.close()

    def get_init_states(self):
        # you can create a file named process ID (example 0.txt, 1.txt, 2.txt) and fill in a set of States
        try:
            file = open(str(self.id) + '.txt', 'r')
        except IOError:
            # if the file is not created, the processes will get the status data
            if self.id == 0:
                return ['A', 'B', 'marker']
            elif self.id == 1:
                return ['F', 'G', 'H']
            else:
                return ['I']
        else:
            with file as f:
                state_lst = [line.strip() for line in f if line]
            return state_lst

    def record_state(self):
        self.__state_storage = self.states[:]
    
    def get_local_snapshot(self):
        return self.__state_storage

    def send_message(self, text_message):
        #if a message is received - "marker" all outgoing messages are saved on the sender and sent using the recover function if necessary
        if self.is_marked and text_message != 'marker':
            self.__message_storage.append(text_message)
            return
        for neighbor in self.neighbors:
            self.channel.queue_declare(queue = str(self.id) + str(neighbor))
            self.channel.basic_publish(exchange = '', routing_key = str(self.id) + str(neighbor), body = text_message)
    
    def recv_message(self):
        for neighbor in self.neighbors:
            queue_title = str(neighbor) + str(self.id)
            for _, _, body in self.channel.consume(queue = queue_title, auto_ack = True):
                message = body.decode('utf-8')
                if message == 'marker':
                    if self.is_marked == False:
                        self.record_state()
                        self.send_message('marker')
                        self.is_marked = True
                        self.send_message('T' + str(self.id))
                        self.send_message('Y' + str(self.id))         
                    else:
                        for _, _, body in self.channel.consume(queue = queue_title, auto_ack = True, inactivity_timeout = 3 ):
                            if body is not None:
                                if body.decode('utf-8') != 'marker':
                                    self.states.append(message)
                            self.channel.cancel()                       
                else:
                    self.states.append(message)
                    #processes expect to receive a message on each incoming channel
                    self.send_message('NM' + str(self.id))
                self.channel.cancel()
    
    def recover(self):
        if self.__message_storage:
            for neighbor in self.neighbors:
                self.channel.queue_declare(queue = str(self.id) + str(neighbor))
                for message in self.__message_storage:
                    self.channel.basic_publish(exchange = '', routing_key = str(self.id) + str(neighbor), body = message)
        
        for neighbor in self.neighbors:
            for _, _, body in self.channel.consume(queue = str(neighbor) + str(self.id), auto_ack = True, inactivity_timeout = 5):
                if body is not None:
                    message = body.decode('utf-8')
                    if message != 'marker':
                        self.states.append(message)
                else:
                    self.channel.cancel()