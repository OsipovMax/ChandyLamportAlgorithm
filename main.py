from process import Process
import threading

# Number of processes in the distributed system model
process_count = 2

def process_work(process: Process) -> None:
    if process.id == 0:
        process.is_initiator = True

def main():
    threads = []
    for i in range(process_count):
        process = Process(i)
        thread = threading.Thread(target=process_work, args=(process,))
        threads.append(thread)
        thread.start()
    for tread in threads:
        tread.join()

if __name__ == "__main__":
    main()