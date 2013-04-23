import time

# This function lets us keep track of slow shit
# It has /some/ execution cost, so we only use it
# on stuff that could kill us if it runs slow, AKA
# World ticks, chunk ticks, etc.
def TickWarn(rate, name=None):
    def deco(func):
        def repl(*args, **kwargs):
            st = time.time()
            val = func(*args, **kwargs)
            et = time.time()
            if et-st > .05*rate:
                print "Call to %s took longer than expected (approx %s ticks)" % (name, (et-st)/.05)
            return val
        return repl
    return deco

class Ticker(object):
    def __init__(self, func, ticks, repeat=False):
        self.func = func
        self.ticks = ticks
        self.repeat = repeat
        self.call_on = -1

    def _rmv(self):
        self.master.rmvTick(self)

    def _add(self, master):
        self.master = master
        self._calc()

    def _calc(self):
        self.call_on = self.master.tick + self.ticks
        if self.call_on > self.master.max_ticks:
            self.call_on = self.master.max_ticks-self.call_on

    def call(self):
        self.func()
        if not self.repeat: self._rmv()
        else: self._calc()

    def __call__(self): return self.func()
