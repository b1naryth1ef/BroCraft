from pymclevel.nbt import *
from proto.packets import Packet
from math import atan2, cos, degrees, radians, pi, sin, sqrt

def getXYZ(args):
    if len(args) == 1: x, y, z = args[0].get()
    else: x, y, z = args
    return int(x), int(y), int(z)

class Position(object):
    kargs = ["x", "y", "z", "yaw", "pitch", "vx", "vy", "vz"]

    def __init__(self, *args, **kwargs):
        if len(args):
            for i in range(0, len(args)):
                self.__dict__[kargs[i]] = args[i]
        elif len(kwargs):
            for k, v in kwargs:
                if k in self.kargs: self.__dict__[k] = v
        else:
            [setattr(self, i, 0) for i in self.kargs]

    def getTeleportPacket(self):
        pk = Packet("teleport")
        pk.x = self.x*32
        pk.y = self.y*32
        pk.z = self.z*32
        pk.yaw, pk.pitch = self.toFracs()
        return pk

    @property
    def bx(self): return self.x*32

    @property
    def by(self): return self.y*32

    @property
    def bz(self): return self.z*32

    def fromLocation(self, l):
        self.x, self.y, self.z = l.get()
        return self

    def fromOrientation(self, o):
        self.yaw, self.pitch = o.get()
        return self

    def fromVelocity(self, v):
        self.vx, self.vy, self.vz = v.get()
        return self

    def toLocation(self):
        return Location(self.x, self.y, self.z)

    def toOrientation(self):
        return Orientation(self.yaw, self.pitch)

    def toVelocity(self):
        return Velocity(self.vx, self.vy, self.vz)

    def modifyPacket(self, p, velo=False, block=False):
        k = ['x', 'y', 'z']
        if velo: [setattr(p, i, getattr(self, "v"+i)) for i in k]
        else: [setattr(p, i, getattr(self, i)) for i in k]
        [setattr(p, i, getattr(self, i)) for i in self.kargs if len(i) > 2]
        return p

    def change(self, k, val):
        self.__dict__[k] += val
        return self

    def fromDegs(self, yaw, pitch):
        self.yaw = radians(yaw) % (pi * 2)
        self.pitch = radians(pitch)

    def toDegs(self):
        return int(round(degrees(self.yaw))), int(round(degrees(self.pitch)))

    def toFracs(self):
        yaw = int(self.yaw * 255 / (2 * pi)) % 256
        pitch = int(self.pitch * 255 / (2 * pi)) % 256
        return yaw, pitch


class PlayerPosition(Position):
    kargs = ["x", "y", "z", "yaw", "pitch", "vx", "vy", "vz", "stance", "grounded"]

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
            i.append(self.tag(getattr(self, x)))
        return TAG_List(i)

    def asList(self):
        return [getattr(self, i) for i in self.key]

    def get(self):
        res = []
        for k in self.key:
            res.append(getattr(self, k))
        return res

    def fromPacket(self, pk):
        for k in self.key:
            setattr(self, k, getattr(pk, k))
        return self

class Location(Locatable):
    key = ['x', 'y', 'z']

    def getRel(self, other):
        x, y, z = self.x-other.x, self.y-other.y, self.z-other.z
        return x, y, z

    def getChunk(self): return int(self.x) >> 4, int(self.z) >> 4
    def __sub__(self, other): # euclidean distance
        x = ((self.x-other.x)**2)
        y = ((self.y-other.y)**2)
        z = ((self.z-other.z)**2)
        return sqrt(x+y+z)

    def __repr__(self):
        return "<Location (%s, %s, %s)>" % self.get()

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

class Velocity(Location):
    key = ['x', 'y', 'z']

class Orientation(Locatable):
    key = ['yaw', 'pitch']
    tag = TAG_Float
