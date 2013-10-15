from worlds.world import World

class WorldManager(object):
    def __init__(self, *worlds):
        self.worlds = dict([(k.id, k) for k in worlds])

    def get(self, id):
        return self.worlds[id]

    def unload(self):
        for i in self.worlds.values():
            if i.loaded: i.unload()

    def load(self):
        for i in self.worlds.values():
            if not i.loaded:
                i.load()

    def tick(self):
        for i in self.worlds.values():
            i.tick()

    def addWorld(self, w):
        if not w.loaded:
            w.load()
            return self.addWorld(w)

    def rmvWorld(self, w):
        if isinstance(w, World):
            w = w.id
        self.worlds[w].unload()
        del self.worlds[w]
