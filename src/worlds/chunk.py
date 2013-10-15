#from entities.manager import EntityManager
from entities.livingentity import LIVING_ENTITIES
from pymclevel.nbt import *
from pymclevel.infiniteworld import packNibbleArray
from proto.packets import Packet
from util.ticks import TickWarn
from numpy import array
from util.log import log

class Chunk(object):
    def __init__(self, world, pos, real):
        self.world = world
        self.pos = pos
        self.c = real
        self.load()

    def getPacket(self): #@TODO Support section-packets to save bandwith?
        inf = []

        if self.c.dirty: self.world.level.generateLights()

        for y in range(0, 256, 16):
            Blocks = self.c.Blocks[..., y:y + 16].swapaxes(0, 2)
            inf.append(array(Blocks, 'uint8').tostring())
        for y in range(0, 256, 16):
            Data = self.c.Data[..., y:y + 16].swapaxes(0, 2)
            inf.append(array(packNibbleArray(Data)).tostring())
        for y in range(0, 256, 16):
            BlockLight = self.c.BlockLight[..., y:y + 16].swapaxes(0, 2)
            inf.append(array(packNibbleArray(BlockLight)).tostring())
        for y in range(0, 256, 16):
            SkyLight = self.c.SkyLight[..., y:y + 16].swapaxes(0, 2)
            inf.append(array(packNibbleArray(SkyLight)).tostring())
        inf.append("\x00" * 256) #@TODO biome data

        p = Packet("chunk")
        p.x, p.z = self.pos
        p.continuous = True
        p.primary = 65535 #@TODO LOL STATIC FTW
        p.add = 0x0
        p.data = "".join(inf)
        return p

    @TickWarn(5, "Chunk Load")
    def load(self, relight=False):
        log.info("Chunk @ %s loading all (%s) entities!" % (str(self.pos), len(self.c.Entities)))
        for ent in self.c.Entities:
            if 'id' not in ent: continue
            if ent['id'].value in LIVING_ENTITIES.keys():
                e = LIVING_ENTITIES[ent['id'].value]().loadFromNbt(ent)
                self.world.em.addEnt(e)

        if relight: self.c.needsLighting = True

    @TickWarn(5, "Chunk Unload")
    def unload(self):
        log.info("Chunk @ %s unloading all (%s) entities!" % (str(self.pos), self.world.em.getNumberInChunk(*self.pos)))
        for ent in self.world.em.getEntsInChunk(*self.pos):
            self.c.Entities.append(ent.saveToNbt())
        self.c.dirty = True

    def suggestUnload(self):
        log.debug("Chunk %s was suggested to unload" % str(self.pos))
        if len([i for i in self.world.game.players.values() if i.entity.getChunk() == self.pos]):
            log.info("Chunk %s is unloading due to lack of players" % str(self.pos))
            self.unload()

    def spawnEntity(self, obj):
        log.debug("Spawning entity %s @ %s" % (obj, str(obj.loc)))
        log.info("Test: %s" % obj.getMetaPacket().build())
        self.world.game.sendNear(obj.getSpawnPacket(), obj.loc, 150) #@TODO is 150 a valid block dist? check mc soruce
        self.world.game.sendNear(obj.getMetaPacket(), obj.loc, 150)
