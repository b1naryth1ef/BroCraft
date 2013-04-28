from proto.packets import Packet
#from proto.util import grounded, position, orientation
from util.pos import Location
#from entities.livingentity import PlayerEntity
from construct import * #@TEMP
import random, time

class Player(object):
    def __init__(self, username, game, client):
        self.client = client
        self.username = username
        self.dispname = username
        self.game = game
        self.server = self.game.server
        self.world = self.game.wm.get(0) #Seems dirty
        self.entity = self.world.loadPlayer(self.username)
        self.loaded_chunks = []

        # Etc
        self.onGround = False

        # Ping/etc
        self.last_ping = 0
        self.ping_key = 0

        # Tick-tracking
        self.callhalf = 0

        # Block Digging
        self.digging = None
        self.dig_start = None

    @property
    def pos(self): return self.entity.pos

    #API stuff
    def canDigBlock(self, loc):
        if loc-self.pos.loc > 6: return False
        return True

    def digBlock(self, loc):
        #block = self.world.getBlock(loc)
        self.world.modifyBlock(0, loc)

    # Packet Parsing
    def positionChange(self, pak): #@TODO eventually implement relative moves
        self.pos.loc.x, self.pos.loc.y, self.pos.loc.z = pak.x, pak.y, pak.z
        self.game.broadcast(self.getTeleportPak(), [self])

    def lookChange(self, pak):
        self.pos.ori.fromDegs(pak.yaw, pak.pitch)
        pk = Packet("entity-orientation", eid=self.entity.id)
        pk.yaw, pk.pitch = self.pos.ori.toFracs()
        self.game.broadcast(pk, [self])
        self.game.broadcast(Packet("entity-head", eid=self.entity.id, yaw=self.pos.ori.toFracs()[0]), [self])

    def groundChange(self, pak): self.onGround = bool(pak.grounded) #@TODO send packet

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

    def getTeleportPak(self):
        x, y, z = self.pos.loc.toRelative()
        pk = Packet("teleport", eid=self.entity.id, x=x, y=y, z=z)
        pk.yaw, pk.pitch = self.pos.ori.toFracs()
        return pk

    def getLocPak(self): #@TODO dis r brok again
        pk = Packet("location")
        self.pos.modifyPacket(pk)
        pk.x = self.pos.x/32.0
        pk.y = self.pos.y/32.0
        pk.z = self.pos.z/32.0
        pk.stance = pk.y+1.62
        pk.grounded = self.onGround
        return pk

    def ping(self, pk):
        if self.ping_key != pk.pid: self.kick("Bad ping response from player.")
        self.last_ping = 0

    def tick(self):
        self.last_ping += 1
        if self.last_ping == 500:
            self.ping_key = random.randint(1, 100)
            self.client.write(Packet("ping", pid=self.ping_key))
        elif self.last_ping > 1000:
            self.kick("Timed out!")

    def tick10(self): #Player List
        self.game.broadcast(Packet("players", username=self.username, online=True, ping=0)) #@TODO ping

    def loadChunk(self, x, z):
        c = self.game.wm.get(0).getChunkAt(x, z, force=True)
        if c:
            self.client.write(c.getPacket())
            self.loaded_chunks.append((x, z))
        else: self.kick("Could not load chunks. <3")

    def login(self):
        #@DEBUG
        self.entity.pos.x = 0
        self.entity.pos.y = 2048 #64
        self.entity.pos.z = 0

        # Login Packet
        pk = Packet("login")
        pk.eid = self.entity.id
        pk.leveltype = "default"
        pk.mode = "survival"
        pk.dimension = "earth"
        pk.difficulty = "normal"
        pk.unused = 0
        pk.maxplayers = self.server.max_players
        self.client.write(pk)

        # Tell the game we have joined
        self.game.playerJoin(self)

        # Preload Chunks in a 10x10 around the player
        self.loadChunkArea(5, 5)

        pk = Packet("compass") #@TODO cleanup
        if self.entity.spawn: pk.x, pk.y, pk.z = self.entity.spawn
        else: pk.x, pk.y, pk.z = (0, 64, 0)
        self.client.write(pk)

        self.client.write(self.getLocPak()) # Spawn the player in

        # Load a larger area for el playero
        #self.loadChunkArea(30, 30)

    def loadChunkArea(self, x, z): # Load/Send chunks in a area around the player
        _x, _z = self.entity.getChunk()
        for cX in range(_x-x, _x+x):
            for cZ in range(_z-z, _z+z):
                print "Sending player chunk @ %s, %s" % (cX, cZ)
                self.loadChunk(cX, cZ)

    def disconnect(self):
        if self.username in self.game.players.keys():
            self.game.playerQuit(self)

    def parseCommand(self, msg): pass
