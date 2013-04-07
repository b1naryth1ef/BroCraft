import random

class EntityManager(object):
    def __init__(self, chunk):
        self.chunk = chunk
        self.ents = {}

    def getEntsInChunk(self, x, y):
        for ent in self.ents.values():
            if int(ent.pos.x) >> 4 == x and int(ent.pos.y) >> 4 == y:
                yield ent

    def generateId(self):
        id = random.randint(111111, 999999)
        if id in self.ents.keys():
            return self.generateId()
        return id

    def addEnt(self, ent, id=None):
        print "Adding entity: %s" % ent
        if not id and ent.id:
            id = ent.id
        if not id:
            id = self.generateId()
        self.ents[id] = ent
        ent.id = id
