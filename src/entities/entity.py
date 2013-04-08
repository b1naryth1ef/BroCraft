from pymclevel.nbt import *
from util.pos import Location, Velocity, Rotation
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
    pos = Location()
    velo = Velocity()
    rotation = Rotation()

    def getChunk(self):
        return (int(self.pos.x >> 4), int(self.pos.z) >> 4)

    def loadFromNbt(self, nbt):
        self.tag = nbt
        self.pos.loadFromNbt(nbt['Pos'])
        self.velo.loadFromNbt(nbt['Motion'])
        self.rotation.loadFromNbt(nbt['Rotation'])

        self.fall_distance = Tag("FallDistance", TAG_Float, 0)
        self.fire_time = Tag("Fire", TAG_Short, 0)
        self.air_time = Tag("Air", TAG_Short, 0)

        self.invulnerable = Tag("Invulnerable", TAG_Byte, 0)
        self.onGround = Tag("OnGround", TAG_Byte, 0)
        self.name = Tag("CustomName", TAG_String, "")

    def saveToNbt(self):
        self.tag['Pos'] = self.pos.saveToNbt()
        self.tag['Motion'] = self.velo.saveToNbt()
        self.tag['Rotation'] = self.rotation.saveToNbt()

        # self.tag['FallDistance'] = TAG_Float(self.fall_distance)
        # self.tag['Fire'] = TAG_Short(self.fire_time)
        # self.tag['Air'] = TAG_Short(self.air_time)

        # self.tag['Invulnerable'] = TAG_Byte(int(self.invulnerable))
        # self.tag['OnGround'] = TAG_Byte(int(self.onGround))
        # self.tag['CustomName'] = TAG_String(self.name)
        #self.tag['CustomNameVisible'] = TAG_Byte(1)
        return self.tag
