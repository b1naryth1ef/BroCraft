from pymclevel.nbt import *
#from proto.packets import Packet
from math import degrees, radians, pi, sqrt

def getXYZ(args):
    if len(args) == 1: x, y, z = args[0].get()
    else: x, y, z = args
    return int(x), int(y), int(z)

class Position(object):
    def __init__(self, location=None, velocity=None, orientation=None):
        self.loc = location
        self.velo = velocity
        self.ori = orientation
        if self.loc: self._buildProps()

    def modifyPacket(self, pak):
        self.loc.modifyPacket(pak)
        self.velo.modifyPacket(pak)
        self.ori.modifyPacket(pak)

    def _buildProps(self): # Fuck this
        self.x = property(self.loc.getX, self.loc.setX)
        self.y = property(self.loc.getY, self.loc.setY)
        self.z = property(self.loc.getZ, self.loc.setZ)

    def onLoad(self, us):
        self.loc = us.loc
        self.velo = us.velo
        self.ori = us.rotation
        if self.loc: self._buildProps()

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

    def modifyPacket(self, pk):
        for k in self.key:
            setattr(pk, k, getattr(self, k))
        return pk

class Location(Locatable):
    key = ['x', 'y', 'z']

    # No one likes -ters, but we need them for property()
    # No really. This looks like shit. :(
    def getX(self): return self.x
    def getY(self): return self.y
    def getZ(self): return self.z
    def setX(self, val): self.x = val
    def setY(self, val): self.y = val
    def setZ(self, val): self.z = val

    def toRelative(self): return self.x*32, self.y*32, self.z*32

    def getChunk(self): return int(self.x) >> 4, int(self.z) >> 4

    def __sub__(self, other): # Euclidean Distance
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

    def fromDegs(self, yaw, pitch):
        self.yaw = radians(yaw) % (pi * 2)
        self.pitch = radians(pitch)
        return self

    def toDegs(self):
        return int(round(degrees(self.yaw))), int(round(degrees(self.pitch)))

    def toFracs(self):
        yaw = int(self.yaw * 255 / (2 * pi)) % 256
        pitch = int(self.pitch * 255 / (2 * pi)) % 256
        return yaw, pitch
