from twisted.internet import protocol, reactor
from net.client import Client

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

        self.protocol = 60
        self.version = "1.5.1"

        self.port = port
        self.max_players = max_players
        self.motd = motd

        self.maintence_msg = ""

    def tick(self): pass

    def isOp(self, username): #@TODO
        if username.lower() == "b1naryth1ef":
            return True
        return False

    def run(self):
        reactor.addSystemEventTrigger('before', 'shutdown', self.game.stopGame)
        reactor.listenTCP(self.port, self.factory)
        reactor.run()
