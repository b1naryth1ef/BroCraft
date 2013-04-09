from pymclevel.nbt import *
from util.pos import Location, Velocity, Orientation, Position
from util.nbtutil import Tag

class Entity(object):
    id = None
    tagid = None
    alive = True
    visible = True
    invulnerable = False
    despawn = False
    age = 0
    # Objects
    pos = Position()
    # Loaders
    loc = Location()
    velo = Velocity()
    rotation = Orientation()

    def getChunk(self):
        return (int(self.pos.x >> 4), int(self.pos.z) >> 4)

    def loadFromNbt(self, nbt):
        self.tag = nbt

        # Location/Orientation/Velocity stuff
        self.loc.loadFromNbt(nbt['Pos'])
        self.velo.loadFromNbt(nbt['Motion'])
        self.rotation.loadFromNbt(nbt['Rotation'])
        self.pos.fromLocation(self.loc).fromVelocity(self.velo).fromOrientation(self.rotation)

        # Static Tags
        self.fall_distance = Tag("FallDistance", TAG_Float, 0)
        self.fire_time = Tag("Fire", TAG_Short, 0)
        self.air_time = Tag("Air", TAG_Short, 0)
        self.invulnerable = Tag("Invulnerable", TAG_Byte, 0)
        self.onGround = Tag("OnGround", TAG_Byte, 0)
        self.name = Tag("CustomName", TAG_String, "")

    def saveToNbt(self):
        self.tag['Pos'] = self.pos.toLocation().saveToNbt()
        self.tag['Motion'] = self.pos.toVelocity().saveToNbt()
        self.tag['Rotation'] = self.pos.toOrientation().saveToNbt()
        return self.tag
