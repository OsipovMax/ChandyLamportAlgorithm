from ds_model import DSModel
from worker import Worker
import pika

# clearing message queues (in case of incorrect behavior)
def clear_rabbitmq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()
    for outcome_point in range(3):
        for income_point in range(3):
            if outcome_point != income_point:
                channel.queue_purge(queue = str(outcome_point) + str(income_point))
    channel.close()
    connection.close()

# creating message queues, if they haven't been created yet
def create_rabbitmq_queues():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
    channel = connection.channel()
    for outcome_point in range(3):
        for income_point in range(3):
            if outcome_point != income_point:
                channel.queue_declare(queue = str(outcome_point) + str(income_point))
    channel.close()
    connection.close()

def main():
    workers = []
    distributed_system_model = DSModel()
    for num in range(distributed_system_model.process_count):
        worker = Worker(num, distributed_system_model)
        workers.append(worker)
        worker.start_work()
    for worker in workers:
        worker.finish_work()
    glob_snapshot = distributed_system_model.get_global_snapshot()
    # if any of the processes did not take a local snapshot, the global snapshot is missing
    if len(glob_snapshot) == 0:
        print('Global snapshot of the system is not made')
    else:
        print('Global snapshot: ', distributed_system_model.get_global_snapshot())
    
if __name__ == "__main__":
    create_rabbitmq_queues()
    main()
    clear_rabbitmq_queues()