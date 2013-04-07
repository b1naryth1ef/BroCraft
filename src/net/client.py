# -*- coding: utf-8 -*-
from twisted.internet import protocol
from proto.packets import PACKETS, Packet
from player import Player
import time

class ClientError(Exception):
    def __init__(self, message):
        self.message = message

class Client(protocol.Protocol):
    def __init__(self, game):
        self.game = game
        self.server = self.game.server
        self.player = None
        self.last_pak = 0

    def authenticate(self): pass #Figure this out later

    def write(self, pak):
        if isinstance(pak, Packet):
            pak = pak.build()
        self.transport.write(pak)

    def dataReceived(self, data):
        try:
            self.parse(data)
        except ClientError, e:
            kp = Packet("dc")
            kp.message = e.message
            self.write(kp)
            self.transport.loseConnection()

    def parse(self, data):
        if data[0] in PACKETS.keys():
            p = Packet(struct=data[0]).read(data[1:])
        elif data[0] != '\n':
            print "Unimplemented Packet: %s" % repr(data[0])
            return
        else: return

        print "Parsing packet '%s'..." % p.name
        self.last_pak = time.time()
        if p.name == "ping" and self.player:
            self.player.ping(p)

        if p.name == "handshake":
            if self.server.maintence_msg and not self.server.isOp(p.username):
                raise ClientError(self.server.maintence_msg)
            if p.protocol != self.server.protocol:
                if p.protocol < self.server.protocol:
                    raise ClientError("Your client is out of date!\n (Server is running %s)" % self.server.version)
                else:
                    raise ClientError("The server is running a older version then your client!\n (Server is running %s)" % self.server.version)
            self.player = Player(p.username, self.game, self)
            self.player.login()

        if p.name == "poll":
            raise ClientError(u"§1\x00%s\x00%s\x00%s\x00%s\x00%s" % (
                self.server.protocol,
                self.server.version,
                self.server.motd,
                len(self.game.players),
                self.server.max_players))

        if p.name == "dc":
            self.connectionLost("quit")

        if p.name == "location": pass
        if p.name == "orientation": pass
        if p.name == "position": self.player.entity.pos.update([p.x, p.y, p.z]) #@TODO Check validity
        if p.name == "chat":
            if p.message.startswith("/"):
                return self.player.parseCommand(p.message)
            if p.message.startswith("@"): pass
            self.game.broadcastMsg("<{yellow}%s{reset}>: %s" % (self.player.username, p.message))

    def connectionLost(self, reason):
        if self.player:
            self.player.disconnect()

        #self.transport.write(data)
