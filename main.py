from server import Server
from client import Client
import threading


class MyThread1(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        s1 = Server('127.0.0.1')
        s1.main_server()


class MyThread2(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        c1 = Client("127.0.0.1")
        c1.main()


# Create new threads
server1 = MyThread1(1, "Thread-1", 1)
client1 = MyThread2(2, "Thread-2", 2)
client2 = MyThread2(2, "Thread-2", 2)
client3 = MyThread2(2, "Thread-2", 2)
client4 = MyThread2(2, "Thread-2", 2)


# Start new Threads
server1.start()
client1.start()
client2.start()
client3.start()
client4.start()

# print("Exiting Main Thread")
