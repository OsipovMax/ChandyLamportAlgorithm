from process import Process

class DSModel:
    def __init__(self, process_count):
        self.process_count = process_count
        self.processes = []

    def generate_model(self):
        for num in range(self.process_count):
            self.processes.append(Process(num))
        self.processes[0].neighbors.append(1)
        self.processes[1].neighbors.append(0)