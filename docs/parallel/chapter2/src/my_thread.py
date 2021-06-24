'''
Date: 2021.06.01 10:58
Description : Omit
LastEditors: Rustle Karl
LastEditTime: 2021.06.01 10:58
'''
import threading
import time

exitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)


def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            import _thread
            _thread.exit()
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


# Create new threads
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Exiting Main Thread")
