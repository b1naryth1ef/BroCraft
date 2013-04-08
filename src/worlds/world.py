from pymclevel import mclevel
from pymclevel.mclevelbase import ChunkNotPresent
from entities.manager import EntityManager
from entities.livingentity import PlayerEntity
from proto.packets import Packet
from util.pos import getXYZ
from worlds.chunk import Chunk

class World(object):
    def __init__(self, game, wid, path, name="world"):
        self.game = game
        self.id = wid
        self.name = name
        self.path = path
        self.level = None
        self.server = None
        self.em = EntityManager(self)

        self.loaded = False
        self.loaded_chunks = {}

        self.spawnX = 0
        self.spawnY = 64
        self.spawnZ = 0

        self.age = None
        self.time = None
        self.gametype = None

    def getBlock(self, *args):
        return self.level.blockAt(getXYZ(args))

    def modifyBlock(self, to, *args):
        x, y, z = getXYZ(args)
        self.level.setBlockAt(x, y, z, to)
        self.game.broadcast(Packet("block", x=x, y=y, z=z, type=to, meta=0))

    def loadPlayer(self, name):
        if name not in self.level.players:
            self.level.createPlayer(name)
        ent = PlayerEntity().loadFromNbt(self.level.getPlayerTag(name))
        self.em.addEnt(ent)
        return ent

    def getChunkAt(self, x, z, force=True):
        if (x, z) not in self.loaded_chunks:
            if not force: return
            if not self.loadChunk(x, z): return
        return self.loaded_chunks[(x, z)]

    def loadChunk(self, x, z):
        print "Loading chunk @ (%s, %s)..." % (x, z),
        try:
            rc = self.level.getChunk(x, z)
            print "DONE!"
        except ChunkNotPresent:
            print "FAILED (Doesnt Exist)"
            return False
        self.loaded_chunks[(x, z)] = Chunk(self, (x, z), rc)
        return True

    def load(self):
        self.level = mclevel.fromFile(self.path)

        self.spawnX = 0 #self.level.root_tag['Data']['SpawnX'].value
        self.spawnY = 64 #self.level.root_tag['Data']['SpawnY'].value
        self.spawnZ = 0 #self.level.root_tag['Data']['SpawnZ'].value

        self.age = self.level.root_tag['Data']['Time'].value
        self.time = self.level.root_tag['Data']['DayTime'].value
        self.gametype = self.level.root_tag['Data']['GameType'].value

        #Load a 5x5 around spawn
        scX, scZ = [int(self.spawnX >> 4), int(self.spawnZ >> 4)]

        for _X in range(scX-5, scX+5):
            for _Z in range(scZ-5, scZ+5):
                self.loadChunk(_X, _Z)

        print "Loaded %s chunks!" % len(self.loaded_chunks)
        self.loaded = True

    def unload(self):
        print "Unloading all chunks..."
        for chunk in self.loaded_chunks.values():
            chunk.unload()
        print "Relighting all chunks..."
        self.level.generateLights()
        print "Saving..."
        self.level.saveInPlace()
        self.level.close()

    def tick(self): pass
