import time
from threading import Thread

def myfunc(i):
    print "sleeping 5 sec from thread %d" % i
    time.sleep(5)
    print "finished sleeping from thread %d" % i

def myfunc2(i):
    print "sleeping beauty 5 sec from thread %d" % i
    time.sleep(5)
    print "finished sleeping handsome from thread %d" % i

for i in range(10):
    t = Thread(target=myfunc, args=(i,))
    t.start()
    t2 = Thread(target=myfunc2, args=((i+1),))
    t2.start()