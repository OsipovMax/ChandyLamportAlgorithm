from process import Process
import threading

class DSModel:
    mutex = threading.Lock()
    def __init__(self):
        #the number of processes is always 3
        self.process_count = 3
        self.active_processes = 3
        self.processes = []
        self.golobal_snapshot = {}
        self.generate_model()
    
    def generate_model(self):
        for num in range(3):
            self.processes.append(Process(num))
            for neighbor in range(3):
                if neighbor != num:
                    self.processes[num].neighbors.append(neighbor)

    def set_global_snapshot(self, process_id, process_snapshot):
        if not process_snapshot:
            return
        self.mutex.acquire()
        self.golobal_snapshot[process_id] = process_snapshot[:]
        self.mutex.release()
    
    def get_global_snapshot(self):
        return self.golobal_snapshot

    def update_sys_status(self):
        self.mutex.acquire()
        self.active_processes -= 1
        self.mutex.release()
    
    def get_sys_status(self):
        return self.active_processes