import thread

class CallAfter(object):
    on = 0
    def __init__(self, amount, call, thread=False, loop=False):
        self.amount = amount
        self.loop = loop
        self.thread = thread
        self.call = call

    def run(self):
        if thread: thread.start_new_thread(self.call, ())
        else: self.call()
        if not self.loop: self.master.tasks.remove(self)
        else: self.on = self.master.tick + self.amount

    def register(self, r):
        self.master = r
        self.on = self.master.tick + self.amount

    def unregister(self):
        self.master.tasks.remove(self)
        self.master = None
