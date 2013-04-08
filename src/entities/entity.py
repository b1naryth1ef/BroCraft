from pymclevel.nbt import *
from util.pos import Location, Velocity, Rotation

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

        self.fall_distance = nbt['FallDistance'].value
        self.fire_time = nbt['Fire'].value
        self.air_time = nbt['Air'].value

        self.invulnerable = bool(nbt['Invulnerable'].value)
        self.onGround = bool(nbt['OnGround'].value)
        self.name = nbt['CustomName'].value

    def saveToNbt(self):
        self.tag['Pos'] = self.pos.saveToNbt()
        self.tag['Motion'] = self.velo.saveToNbt()
        self.tag['Rotation'] = self.rotation.saveToNbt()

        self.tag['FallDistance'] = TAG_Float(self.fall_distance)
        self.tag['Fire'] = TAG_Short(self.fire_time)
        self.tag['Air'] = TAG_Short(self.air_time)

        self.tag['Invulnerable'] = TAG_Byte(int(self.invulnerable))
        self.tag['OnGround'] = TAG_Byte(int(self.onGround))
        self.tag['CustomName'] = TAG_String(self.name)
        #self.tag['CustomNameVisible'] = TAG_Byte(1)
        return self.tag
