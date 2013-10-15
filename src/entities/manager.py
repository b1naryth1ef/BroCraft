from util.log import log
import random

class EntityManager(object):
    def __init__(self, chunk):
        self.chunk = chunk
        self.ents = {}

    def getEntsInChunk(self, x, y):
        for ent in self.ents.values():
            if int(ent.pos.getX()) >> 4 == x and int(ent.pos.getY()) >> 4 == y:
                yield ent

    def generateId(self):
        id = random.randint(111111, 999999)
        if id in self.ents.keys():
            return self.generateId()
        return id

    def addEnt(self, ent, id=None):
        log.debug("Attempting to add entity: %s" % ent)
        if not id and ent.id: id = ent.id
        if not id: id = self.generateId()
        self.ents[id] = ent
        ent.id = id

    def getNumberInChunk(self, x, y):
        return len([None for i in self.getEntsInChunk(x, y)])

    def getNumber(self):
        return len(self)

    def __len__(self):
        return len(self.ents)

    def __iter__(self):
        return self.ents.values()
