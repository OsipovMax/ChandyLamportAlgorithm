from process import Process
import threading


class Worker:
    def __init__(self, id, dstr_sys_model):
        self.worker_thread_id = id
        self.worker_thread = threading.Thread(
            target=self.work_target, args=(dstr_sys_model,)
        )

    # this is basic fucntion for worker
    def work_target(self, dstr_sys_model):
        process = dstr_sys_model.processes[self.worker_thread_id]
        init_states = process.get_init_states()
        # only a process with id = 0 initiates the snapshot
        if process.id == 0:
            for state in init_states:
                if state == "marker":
                    process.is_initiator = True
                    process.is_marked = True
                    process.record_state()
                    process.send_message("marker")
                    process.recv_message()
                else:
                    process.states.append(state)
            # there was no marker, just passing a message to your neighbors
            if process.is_initiator == False:
                # something send
                process.send_message("NM" + str(process.id))
                # something recv
                process.recv_message()
        elif process.id == 1:
            if "marker" in init_states:
                init_states.remove("marker")
            process.states = init_states
            process.recv_message()
        elif process.id == 2:
            if "marker" in init_states:
                init_states.remove("marker")
            process.states = init_states
            process.recv_message()
        # modeling the system drop
        dstr_sys_model.update_sys_status()
        while True:
            # distribution system is drop
            if dstr_sys_model.get_sys_status() == 0:
                break
        if process.is_marked:
            process.recover()
            print("channel state", process._message_storage)
        print("Results of the process - ", process.id, ": ", process.states)
        dstr_sys_model.set_global_snapshot(
            process.id, process.get_local_snapshot(), process._message_storage
        )
        process.close_connection()

    def start_work(self):
        self.worker_thread.start()

    def finish_work(self):
        self.worker_thread.join()
