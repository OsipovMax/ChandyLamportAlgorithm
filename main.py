from process import Process
from ds_model import DSModel
import threading

# Number of processes in the distributed system model
process_count = 2

def process_work(process: Process) -> None:
    if process.id == 0:
        #initiator snapshot
        process.is_initiator = True
        process.record_state()
        print(process.id)
        return
    print(process.id)

def main():
    threads = []
    distributed_system_model = DSModel(process_count)
    distributed_system_model.generate_model()
    for num in range(process_count):
        thread = threading.Thread(target=process_work, args=(distributed_system_model.processes[num],))
        threads.append(thread)
        thread.start()
    for tread in threads:
        tread.join()

if __name__ == "__main__":
    main()