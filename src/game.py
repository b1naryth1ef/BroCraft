from net.server import Server
from worlds.manager import WorldManager
from worlds.world import World
from proto.packets import Packet, CombPacket
from util.color import colorize
from util.ticks import Ticker
from util.log import log
from util.thread import ThreadManager
import time, thread

#DEBUG
from inventory.itemstack import ItemStack
from inventory.material import mm

class Game(object):
    def __init__(self):
        self.server = Server(self)
        self.players = {}
        self.ticks = []

        self.tick = 0
        self.max_ticks = 50000000 # Random number ftw

        w = World(self, 0, "/home/b1nzy/.minecraft/saves/asdfasdf/level.dat")
        self.wm = WorldManager(w)
        self.tm = ThreadManager()

        self.running = False
        self.callTen = self.addTick(Ticker(self.call10, 10, True))

    def addTick(self, t):
        self.ticks.append(t)
        t._add(self)
        return t

    def rmvTick(self, t):
        if t in self.ticks: self.ticks.remove(t)

    def call10(self):
        for plyr in self.players.values():
            plyr.tick10()

    def tickLoop(self):
        while self.running:
            time.sleep(0.05)
            self.tick += 1
            if self.tick > self.max_ticks: self.tick = 0
            for plyr in self.players.values():
                plyr.tick()
            for t in self.ticks:
                if t.call_on == self.tick:
                    try: t.call()
                    except Exception, e: log.warning("Exception in a Ticker call! (%s)" % e)

    def runGame(self):
        log.debug("Game starting!")
        self.running = True
        self.wm.load()
        thread.start_new_thread(self.tickLoop, ())
        self.server.run()

    def stopGame(self):
        log.debug("Game stopping!")
        self.running = False
        self.wm.unload()

    def broadcast(self, pak, ignore=[]):
        for p in self.players.values():
            if p in ignore: continue
            p.client.write(pak)

    def broadcastMsg(self, msg):
        log.debug("Broadcasting message: %s" % msg)
        self.broadcast(Packet("chat", message=colorize(msg)))

    def sendNear(self, pak, loc, dist):
        count = 0
        for p in self.players.values():
            if loc-p.pos.loc < dist:
                p.client.write(pak)
                count += 1
        return bool(count)

    def playerJoin(self, p):
        log.debug("Player join: %s" % p.username)
        self.broadcast(Packet("players", username=p.username, online=True, ping=0))
        if len(self.players):
            # Tell other players we exist
            pk = p.getSpawnPacket()
            self.broadcast(pk, ignore=[p])
            # Load other players for us
            for i in self.players.values():
                p.client.write(i.getSpawnPacket())
        self.players[p.username] = p
        self.broadcastMsg("{yellow}%s joined the game" % p.username)

    def test(self):
        #@DEBUG
        it = ItemStack(mm.DIRT, 64).toEntity()
        c = self.wm.worlds[0].loaded_chunks[(0, 0)]
        it.loc.x = 0
        it.loc.y = 64
        it.loc.z = 0
        c.spawnEntity(it)

    def playerQuit(self, p):
        del self.players[p.username]
        self.broadcastMsg("{yellow}%s quit the game" % p.username)
        #@TODO unload chunks
