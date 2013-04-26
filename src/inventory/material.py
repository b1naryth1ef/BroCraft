from inventory.block import Block

class Material(object):
    def __init__(self, id, name="none", obj=Block):
        self.id = id
        self.name = name
        self.obj = obj

    def build(self, loc):
        return self.obj(self.id, loc)

class MaterialManager(object):
    name_map = {}
    id_map = {}

    def build(self):
        for k, v in self.__dict__.items():
            if k.isupper():
                self.name_map[v.name] = v
                self.id_map[v.id] = v

    def getMaterialByID(self, id):
        if id in self.id_map.keys(): return self.id_map[id]

    def getMaterialByName(self, name):
        if name.lower() in self.name_map.keys(): return self.name_map[name.lower()]


# @TODO finish this off
mm = MaterialManager()
mm.AIR = Material(0, "air", None)
mm.STONE = Material(1, "stone")
mm.GRASS = Material(2, "grass")
mm.DIRT = Material(3, "dirt")
mm.build()
