from net.server import Server
from worlds.manager import WorldManager
from worlds.world import World
from proto.packets import Packet, CombPacket
from util.color import colorize

import time, thread, random

class Game(object):
    def __init__(self):
        self.server = Server(self)
        self.players = {}

        w = World(self, 0, "/home/andrei/.minecraft/saves/world/level.dat")
        self.wm = WorldManager(w)

        self.running = False

    def tickLoop(self):
        while self.running:
            time.sleep(0.05)
            for plyr in self.players.values():
                plyr.tick()

    def runGame(self):
        self.running = True
        self.wm.load()
        thread.start_new_thread(self.tickLoop, ())
        self.server.run()

    def stopGame(self):
        self.running = False
        self.wm.unload()
        print "Done!"

    def broadcast(self, pak):
        for p in self.players.values():
            p.client.write(pak)

    def broadcastMsg(self, msg):
        self.broadcast(Packet("chat", message=colorize(msg)))

    def playerJoin(self, p):
        if len(self.players):
            pk1 = Packet("create", eid=p.entity.id)
            pk2 = Packet("player", eid=p.entity.id, username=p.username, x=int(p.pos.x), y=int(p.pos.y), z=int(p.pos.z), yaw=0, pitch=0, item=0, metadata={})
            self.broadcast(CombPacket(pk1, pk2))
        self.players[p.username] = p
        self.broadcastMsg("{yellow}%s joined the game" % p.username)

    def playerQuit(self, p):
        del self.players[p.username]
        self.broadcastMsg("{yellow}%s quit the game" % p.username)
        #@TODO unload chunks
