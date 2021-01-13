import time
import signal
import os
from multiprocessing import Queue, Pipe, Process, Manager
from threading import Thread, get_ident

def multiprocess_timecheck(func):
    def wrapper(*args):
        print("func is : ", func)
        print("*args is : ", *args)
        print("args is : ", args)
        # 입력은 아마 (self, queue, 각 변수) 로 들어오게 됨.
        parent_pipe, children_pipe = Pipe()
        thread = Thread(target=response_waiter, args=(children_pipe, func, *args))
        thread.start()
        thread.join()
        value = parent_pipe.recv()
        print(value)
        return value
    return wrapper

def response_waiter(pipe, func, *args):
    thread_id = get_ident()
    args[1].put([thread_id, pipe, func, *args])     # 이게 Queue에 들어가게 되는 것!
    signal.sigwait([signal.SIGUSR1])


class CoinoneQueue:

    def __init__(self):
        self.private_queue = Queue()
        self.public_queue = Queue()
        self.private_timequeue = Process(target=self._get_from_queue, args=(self.private_queue, 0.13))
        self.public_timequeue = Process(target=self._get_from_queue, args=(self.public_queue, 0.25))
        self.private_timequeue.start()
        self.public_timequeue.start()

    # 얘가 Process로 돌면서 처리해야 함
    def _get_from_queue(self, queue: Queue, sleep_time: float):
        after_time = time.time()
        while True:
            value = queue.get()     # pid 번호만 받음
            # print(value)

            recv_time = time.time()
            timediff = recv_time - after_time
            if timediff < sleep_time:
                time.sleep(sleep_time - timediff)
            after_time = time.time()
            # print(after_time, sleep_time)

            os.kill(value, signal.SIGUSR1)
            # print("Finished!")


