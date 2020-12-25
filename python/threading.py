import threading

#Code pulled from: https://stonesoupprogramming.com/2017/08/30/python-threading/

# Thread is the base class for creating OOP Style Threads
# It has a run() method that contains the code that runs in a new thread
class Threading(threading.Thread):
    def __init__(self, myId, count, mutex):
        self.myId = myId
        self.count = count
        self.mutex = mutex
        threading.Thread.__init__(self)

    # Everything inside of run is executed in a seperate thread
    def run(self):
        for i in range(self.count):
            with self.mutex:
                print('[{}] => {}'.format(self.myId, i))


if __name__ == '__main__':
    stdoutmutex = threading.Lock()
    threads = []
    for i in range(10):
        # Create the new Thread Object
        thread = MyThread(i, 100, stdoutmutex)

        # The thread doesn't actually start running until
        # start() is called
        thread.start()
        threads.append(thread)

    for thread in threads:
        # join() is used to synchronize threads
        # Calling join() on a thread makes the parent thread wait
        # until the child thread has finished
        thread.join()

    print('Main thread exiting...')
