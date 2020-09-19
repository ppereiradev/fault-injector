import multiprocessing as mp
import time

def f(name):
    count = 0
    while True:    
        print('hello ', name, "count: ", count)
        count += 1
        time.sleep(1)

if __name__ == '__main__':
    p = mp.Process(target=f, args=('bob',))
    p.start()
    print("main process going to sleep")
    time.sleep(5)
    p2 = mp.Process(target=f, args=('paulo',))
    p2.start()
    print("main process going to sleep again")
    time.sleep(5) 
    c = 0
    while True:
        print("main")
        time.sleep(1)
        c += 1
        if c == 10:
            print("matar processing")
            p.terminate()
