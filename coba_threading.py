import threading
import os
import time

def task1():
    print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 1: {}".format(os.getpid()))
    i=0
    while(1):
        time.sleep(1)
        i = i+1
        print(i)
        if(i>100):
            break
        

def task2():
    print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
    print("ID of process running task 2: {}".format(os.getpid()))
    i=0
    while(1):
        time.sleep(1)
        i = i+2
        print(i)
        if(i>100):
            break
        

if __name__ == "__main__":

    print("ID of process running main program: {}".format(os.getpid()))

    print("Main thread name: {}".format(threading.current_thread().name))

    t1 = threading.Thread(target=task1, name='t1')
    t2 = threading.Thread(target=task2, name='t2')

    t1.start()
    t2.start()

    #.join digunakan untuk menunggu thread selesais
    t1.join()
    t2.join()
    
    