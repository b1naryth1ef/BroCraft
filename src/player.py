from proto.packets import Packet
from proto.util import grounded, position, orientation
from util.pos import Location
from entities.livingentity import PlayerEntity
from construct import * #@TEMP
import random, time

class Player(object):
    def __init__(self, username, game, client):
        self.client = client
        self.username = username
        self.game = game
        self.server = self.game.server
        self.world = self.game.wm.get(0) #Seems dirty
        self.entity = self.world.loadPlayer(self.username)

        self.game.playerJoin(self)
        #self.game.players[self.username] = self

        self.loaded_chunks = []

        #Ping/etc
        self.last_ping = 0
        self.ping_key = 0

        #Block Digging
        self.digging = None
        self.dig_start = None

    @property
    def pos(self): return self.entity.pos

    #API stuff
    def canDigBlock(self, loc):
        if loc-self.entity.pos > 6: return False
        return True

    def digBlock(self, loc):
        #block = self.world.getBlock(loc)
        self.world.modifyBlock(0, loc)

    # Packet Parsing
    def locationChange(self, pak): pass
    def lookChange(self, pak): pass
    def dig(self, pak):
        loc = Location(pak.x, pak.y, pak.z)
        if pak.state == 'started':
            self.digging = loc
            self.dig_start = time.time()
        elif pak.state == 'stopped':
            if self.digging and self.digging == loc:
                if self.canDigBlock(loc): #@TODO check break time
                    self.digBlock(loc)
        elif pak.state == 'cancelled':
            self.digging = None
            self.dig_start = None

    def kick(self, msg):
        self.client.write(Packet("dc", message=msg))

    def getLocPak(self): #@TEMP
        pk = Packet("location")
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
        c = self.game.wm.get(0).getChunkAt(x, z, force=True)
        if c:
            self.client.write(c.getPacket())
            self.loaded_chunks.append((x, z))
        else:
            print "DERP"

    def login(self):
        self.entity.pos.x = 0
        self.entity.pos.y = 64
        self.entity.pos.z = 0

        pk = Packet("login")
        pk.eid = self.entity.id
        pk.leveltype = "default"
        pk.mode = "survival"
        pk.dimension = "earth"
        pk.difficulty = "normal"
        pk.unused = 0
        pk.maxplayers = self.server.max_players
        self.client.write(pk)

        #Load Chunks in a 20x20 around the player
        x, z = self.entity.getChunk()
        for cX in range(x-5, x+5):
            for cZ in range(z-5, z+5):
                print "Sending player chunk @ %s, %s" % (cX, cZ)
                self.loadChunk(cX, cZ)

        pk = Packet("compass")
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
