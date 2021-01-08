import threading
import multiprocessing

#Code pulled from: https://stonesoupprogramming.com/2017/08/30/python-threading/

# Thread is the base class for creating OOP Style Threads
# It has a run() method that contains the code that runs in a new thread
class MyThread(threading.Thread):
    '''
    Overwrites python's default threading agent so we can use it with OOP.
    I kinda wish that I could do this with multiprocessing.
    '''
    def __init__(self, func, *args):
        '''
        Variables that get created to pass to the function that wiill run.
        Includes pointer to function and the args that get passed.
        '''
        threading.Thread.__init__(self)
        #super(MyThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.stdoutmutex = threading.Lock()
        self.function_call = func
        print(args)
        self.arguments = args[0][1]
        self.classref = args[0][0]


    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    # Everything inside of run is executed in a seperate thread
    def run(self):
        try:
            #calls the function gives the function a ref to thread.
            #print(self.function_call, self.arguments)
            self.function_call(self.classref, self.arguments, self)
        except Exception as e:
            print("In thread handler their was an error.")
            print(e)

class Thread_Handler():
    thread_list = []

    def __init__(self, universe):
        self.universal = universe

    def delete(self):
        print("Waiting for threads to exit...")
        for thread in self.thread_list:
            thread.stop()
        for thread in self.thread_list:
            thread.join()

    def run_in_thread(self, func, *args):
        new_thread = MyThread(func, args)
        new_thread.start()
        self.thread_list.append(new_thread)

    def remove_thread(self, thread_pointer):
        if thread_pointer in self.thread_list:
            thread_pointer.stop()
            thread_pointer.join()
            self.thread_list.pop(thread_pointer)
