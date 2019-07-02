from multiprocessing import Process, Queue
import time

def f(q):
    time.sleep(2)
    q.put(42)
    q.put(None)
    q.put('hello')

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()

    counter = 0
    while 1:
        try:
            print(q.get(False))    # prints "[42, None, 'hello']"
            break
        except:
            print(counter)
            counter+=1
    p.join()
