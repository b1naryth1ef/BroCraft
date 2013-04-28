from inventory.material import Material, mm
from entities.entity import Item

class ItemStack(object):
    def __init__(self, id, amount=1, damage=0, data=0x0):
        self.amount = amount
        self.damage = damage
        self.data = data

        self.dura = 1

        if isinstance(id, Material): self.id = id
        else:
            self.id = mm.getMaterialByID(int(id)) #@DEV int for dirty str support
            if not self.id: raise Exception("Invalid item id (%s) in ItemStack constructor!" % id)

    def toEntity(self):
        e = Item()
        e.id = self.id.id
        e.damage = self.damage
        e.count = self.amount
        e.age = 0
        e.health = 1 #@TODO what should this be? I assume 0 = dead
        return e
