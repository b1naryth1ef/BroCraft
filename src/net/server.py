from twisted.internet import protocol, reactor
from net.client import Client
from util.log import log

class ServerFactory(protocol.Factory):
    def __init__(self, game):
        self.game = game

    def buildProtocol(self, addr):
        c = Client(self.game)
        c.factory = self
        return c

class Server(object):
    def __init__(self, game, port=25565, max_players=16, motd="BroCraft!"):
        self.game = game
        self.factory = ServerFactory(self.game)

        self.protocol = 61
        self.version = "1.5.2"

        self.port = port
        self.max_players = max_players
        self.motd = motd

        self.maintence_msg = ""

    def tick(self): pass

    def isOp(self, username): #@TODO
        if username.lower() in ["b1naryth1ef", "spekode"]:
            return True
        return False

    def run(self):
        log.info("Server Starting up!")
        reactor.addSystemEventTrigger('before', 'shutdown', self.game.stopGame)
        reactor.listenTCP(self.port, self.factory)
        log.info("Server running...")
        reactor.run()

class DebugClient(protocol.Protocol):
    def dataReceived(self, data):
        log.debug("Got a line! such wow!")
        with open("output.txt", "ab") as f:
            f.write(data)

class DebugFactory(protocol.Factory):
    def buildProtocol(self, addr):
        c = DebugClient()
        c.factory = self
        return c

class DebugServer(object):
    def __init__(self, port=25565):
        self.factory = DebugFactory()
        self.port = port

    def run(self):
        reactor.listenTCP(self.port, self.factory)
        reactor.run()
