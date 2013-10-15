# -*- coding: utf-8 -*-
from twisted.internet import protocol
from proto.packets import PACKETS, Packet, PacketBase, parse_packets
from protolib.lib import getPacket, decode
from player import Player
from util.log import log

from net import Buff

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
        self.buffer = Buff()

        # Is the connection init'd
        self.started = False

    def authenticate(self): pass #Figure this out later

    def write(self, pak):
        if self.player and not self.player.connected:
            log.warning("Client.write failed due to the player (%s) being disconnected!" % self.player.username)
        if isinstance(pak, PacketBase):
            pak = pak.build()
        self.transport.write(pak)

    def dataReceived(self, data):
        self.buffer.push_multi(data)

        if not self.started:
            log.debug("trying...")
            val = decode(self.buffer, force_as=getPacket("handshake"))
            if val:
                log.debug("Got handshake!")
                self.started = True
                return

        packet = decode(self.buffer)
        if not packet:
            log.warning("No packet found (Right now this breaks everything :( )")
            continue
        log.info("Found packet %s" % packet.name)
        #self.transport.loseConnection()

    def parse(self):
        """
        Attempt to parse the buffer
        """
        val = decode(self.buffer)
        if not val:
            return
        log.debug("PARSED: %s" % val.name)

    def parseOne(self, p):
        if p.name not in ['grounded', 'position']:
            log.debug("Parsing Packet %s" % p.name)
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

        if p.name == "dc": self.connectionLost("quit")

        # Blocks/Modify
        if p.name == "digging": self.player.dig(p)

        # Movement
        if p.name == "orientation" or p.name == "location":
            self.player.lookChange(p)
            self.player.groundChange(p)
        if p.name == "position" or p.name == "location":
            self.player.positionChange(p)
            self.player.groundChange(p)

        # Chat
        if p.name == "chat":
            if p.message.startswith("/"): return self.player.parseCommand(p.message)
            if p.message.startswith("@"): pass
            self.game.broadcastMsg("<{yellow}%s{reset}>: %s" % (self.player.username, p.message))

    def connectionLost(self, reason):
        if self.player:
            self.player.disconnect()

        #self.transport.write(data)
