from threading import Thread
from util.log import log
import time

class BroThread(Thread):
    def __init__(self, f, a, k, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self._exec = f
        self._args = a
        self._kargs = k

    def run(self):
        self._exec(*self._args, **self._kargs)

class BroTimedThread(BroThread):
    start, end = 0, 0

    def run(self):
        self.start = time.time()
        BroThread.run(self)
        self.end = time.time()

    def get(self):
        return self.end-self.start

class ThreadManager(object):
    def __init__(self, limit=500):
        self.threads = []
        self.limit = limit

    def run(self, f, *args, **kwargs):
        log.debug("Starting new thread for function %s" % f)
        t = BroThread(f, args, kwargs)
        self.threads.append(t)
        t.start()
        return t

    def runTimed(self, f, *args, **kwargs):
        log.debug("Starting new timed thread for function %s" % f)
        t = BroTimedThread(f, args, kwargs)
        self.threads.append(t)
        t.start()
        return t
