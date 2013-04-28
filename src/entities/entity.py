from pymclevel.nbt import *
from util.pos import Location, Velocity, Orientation, Position
from util.nbtutil import Tag
from proto.packets import Packet

class Entity(object):
    id = None
    tagid = None
    alive = True
    visible = True
    invulnerable = False
    despawn = False
    age = 0
    # Hybrid Classes
    pos = Position()

    # Loaders
    loc = Location()
    velo = Velocity()
    rotation = Orientation()

    def __init__(self):
        self.loc = Location(0, 0, 0)
        self.velo = Velocity(0, 0, 0)
        self.rotation = Orientation(0, 0)
        self.pos.onLoad(self)

    def getChunk(self):
        return (int(self.pos.x >> 4), int(self.pos.z) >> 4)

    def loadFromNbt(self, nbt):
        self.tag = nbt

        # Location/Orientation/Velocity stuff
        self.loc.loadFromNbt(nbt['Pos'])
        self.velo.loadFromNbt(nbt['Motion'])
        self.rotation.loadFromNbt(nbt['Rotation'])

        # Load Hybrid Position Holder
        self.pos.onLoad(self)

        # Static Tags
        self.fall_distance = Tag("FallDistance", TAG_Float, 0)
        self.fire_time = Tag("Fire", TAG_Short, 0)
        self.air_time = Tag("Air", TAG_Short, 0)
        self.invulnerable = Tag("Invulnerable", TAG_Byte, 0)
        self.onGround = Tag("OnGround", TAG_Byte, 0)
        self.name = Tag("CustomName", TAG_String, "")

    def saveToNbt(self):
        return self.tag

class BaseItem(Entity):
    def loadFromNbt(self, nbt):
        Entity.loadFromNbt(self, nbt)

        self.health = Tag("Health", TAG_Short, 0)
        self.age = Tag("Age", TAG_Short, 0)

class Item(BaseItem): #@TDOO "tag" logic for loading extra info
    entity_type = 2
    def loadFromNbt(self, nbt):
        BaseItem.loadFromNbt(self, nbt)

        self.id = Tag('Id', TAG_Short, 1)
        self.damage = Tag("Damage", TAG_Short, 0)
        self.count = Tag("Count", TAG_Byte, 0)

        return self

    def getSpawnPacket(self):
        p = Packet("spawn")
        p.eid = self.id
        p.type = self.entity_type
        p.x = self.loc.x
        p.y = self.loc.y
        p.z = self.loc.z
        p.pitch = self.rotation.pitch
        p.yaw = self.rotation.yaw
        p.data = 1 #@DEV what does this do?
        return p

class XPOrb(BaseItem): pass
