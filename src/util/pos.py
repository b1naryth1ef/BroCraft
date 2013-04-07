from pymclevel.nbt import *
from proto.util import position

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

class Velocity(Location):
    key = ['x', 'y', 'z']

class Rotation(Locatable):
    key = ['yaw', 'pitch']
    tag = TAG_Float
