import threading
import time

exitFlag = 0

test_thread_lock = threading.Lock()
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
#        test_thread_lock.acquire()
        with test_thread_lock:
            print ("{}: {}".format(threadName, time.ctime(time.time())))
#        test_thread_lock.release()
        counter -= 1

def test_simple_multi_thread():
    # start thread without create a class
    ts = []
    for i in range(1, ):
        t = threading.Thread(target=print_time, args=("Thread-"+str(i), 0.5, 5))
        t.start()
        ts.append(t)

    for t in ts:
        t.join()

class TestThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print_time(self.name, 0.5, self.counter)

def test_multi_thread_locking():
    ts = []
    for i in range(1, 10):
        t = TestThread(i, "Thread-"+str(i), 5)
        t.start()
        ts.append(t)

    for t in ts:
        t.join()

    print("thread count:", threading.active_count())

test_simple_multi_thread()
# test_multi_thread_locking()

