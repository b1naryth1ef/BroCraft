from proto.packets import Packet
from proto.util import grounded, position, orientation
from entities.livingentity import PlayerEntity
from construct import * #@TEMP
import random

class Player(object):
    def __init__(self, username, game, client):
        self.client = client
        self.username = username
        self.game = game
        self.server = self.game.server
        self.entity = self.game.wm.get(0).loadPlayer(self.username)

        self.game.playerJoin(self)
        #self.game.players[self.username] = self

        self.loaded_chunks = []

        #Ping/etc
        self.last_ping = 0
        self.ping_key = 0

    def kick(self, msg):
        self.client.write(Packet("dc", message=msg))

    def getLocPak(self): #@TEMP
        pk = Packet("location")
        self.entity.pos.x = 0
        self.entity.pos.y = 64
        self.entity.pos.z = 0
        pk.x, pk.y, pk.z = self.entity.pos.asList()
        pk.stance = 0
        pk.rotation = 1.0
        pk.pitch = 1.0
        pk.grounded = 1
        return pk

    def ping(self, pk):
        if self.ping_key != pk.pid: self.kick("Bad ping response from player.")
        self.last_ping = 0

    def tick(self):
        self.last_ping += 1
        if self.last_ping == 500:
            self.ping_key = random.randint(1, 100)
            self.client.write(Packet("ping", pid=self.ping_key)) #@TODO pid
        elif self.last_ping > 1000:
            self.kick("Timed out!")

    def loadChunk(self, x, z):
        c = self.game.wm.get(0).getChunkAt(x, z)
        if c: self.client.write(c.getPacket())
        self.loaded_chunks.append((x, z))

    def login(self):
        pk = Packet("login")
        print self.entity.id
        pk.eid = 0#self.entity.id
        pk.leveltype = "default"
        pk.mode = "creative"
        pk.dimension = "earth"
        pk.difficulty = "normal"
        pk.unused = 0
        pk.maxplayers = self.server.max_players
        self.client.write(pk)

        #Load Chunks in a 10x10 around the player
        for cX in range(int(self.entity.pos.x)-5, int(self.entity.pos.x)+5):
            for cZ in range(int(self.entity.pos.z)-5, int(self.entity.pos.z)+5):
                self.loadChunk(cX, cZ)

        pk = Packet("spawn")
        if self.entity.spawn:
            pk.x, pk.y, pk.z = self.entity.spawn
        else:
            pk.x, pk.y, pk.z = (0, 64, 0)
        self.client.write(pk)

        self.client.write(self.getLocPak())

    def disconnect(self):
        if self.username in self.game.players.keys():
            self.game.playerQuit(self)

    def parseCommand(self, msg): pass
