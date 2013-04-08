from pymclevel.nbt import *
#from proto.util import position
import math

def getXYZ(args):
    if len(args) == 1: x, y, z = args[0].get()
    else: x, y, z = args
    return x, y, z

class Locatable(object):
    key = []
    tag = TAG_Double

    def __init__(self, *locs):
        if locs: self.update(locs)

    def update(self, locs):
        for pos, i in enumerate(self.key):
            self.__dict__[i] = locs[pos]

    def loadFromNbt(self, tag):
        self.update([i.value for i in tag.value])

    def saveToNbt(self):
        i = []
        for pos, x in enumerate(self.key):
            i.append(self.tag(self.__dict__[x]))
        return TAG_List(i)

    def asList(self):
        return [self.__dict__[i] for i in self.key]

class Location(Locatable):
    key = ['x', 'y', 'z']

    def get(self): return self.x, self.y, self.z
    def getChunk(self): return int(self.x) >> 4, int(self.z) >> 4
    def __sub__(self, other): # euclidean distance
        x = ((self.x-other.x)**2)
        y = ((self.y-other.y)**2)
        z = ((self.z-other.z)**2)
        return math.sqrt(x+y+z)

    def __repr__(self):
        return "<Location (%s, %s, %s)>" % self.get()

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

class Velocity(Location):
    key = ['x', 'y', 'z']

class Rotation(Locatable):
    key = ['yaw', 'pitch']
    tag = TAG_Float
