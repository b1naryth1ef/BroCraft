from entities.entity import Entity
from pymclevel.nbt import *
from util.nbtutil import Tag

class LivingEntity(Entity):
    max_health = 0
    def loadFromNbt(self, nbt):
        Entity.loadFromNbt(self, nbt)
        return self

    def saveToNbt(self):
        Entity.saveToNbt(self)
        return self.tag

class Breedable(LivingEntity):
    def loadFromnbt(self, nbt):
        LivingEntity.loadFromNbt(self, nbt)

        self.loveTime = nbt['InLove'].value
        self.age = nbt['Age'].value
        self.owner = nbt['Owner'].value
        self.sitting = bool(nbt['Sitting'].value)

        return self

    def saveTonbt(self):
        LivingEntity.saveToNbt(self)

        self.tag['InLove'] = TAG_Int(self.inLove)
        self.tag['Age'] = TAG_Int(self.age)
        self.tag['Owner'] = TAG_String(self.owner)
        self.tag['Sitting'] = TAG_Byte(int(self.sitting))

        return self.tag

class Chicken(Breedable):
    max_health = 4
    tagid = "Chicken"

    def loadFromNbt(self, nbt):
        Breedable.loadFromNbt(self, nbt)

        self.health = nbt['Health'].value
        self.active_effects = None #@TODO

        return self

    def saveToNbt(self):
        Breedable.saveToNbt(self)
        self.tag['Health'] = TAG_Short(self.health)
        return self.tag

class PlayerEntity(LivingEntity):
    max_health = 16
    tagid = "Player"

    def loadFromNbt(self, nbt):
        LivingEntity.loadFromNbt(self, nbt)

        self.dim = Tag("Dimension", TAG_Int, 0)
        self.gametype = Tag("playerGameType", TAG_Int, 0)
        self.score = Tag("Score", TAG_Int, 0)
        self.slot = Tag("SelectedItemSlot", TAG_Int, 9)
        self.foodLevel = Tag("foodLevel", TAG_Int, 0)
        self.foodExhaustionLevel = Tag("foodExhaustionLevel", TAG_Float, 0)
        self.foodSaturationLevel = Tag("foodSaturationLevel", TAG_Float, 0)
        self.foodTickTimer = Tag("foodTickTimer", TAG_Int, 0)
        self.xpLevel = Tag("XpLevel", TAG_Int, 0)
        self.xpPercent = Tag("XpP", TAG_Float, 0)
        self.xpTotal = Tag("XpTotal", TAG_Int, 0)
        if 'SpawnX' in nbt: self.spawn = (nbt['SpawnX'].value, nbt['SpawnY'].value, nbt['SpawnZ'].value)
        else: self.spawn = None
        #@TODO inventories & abilities

        return self

    def saveToNbt(self, nbt):
        LivingEntity.saveToNbt(self, nbt)

        if self.spawn:
            nbt['SpawnX'] = TAG_Int(self.spawn[0])
            nbt['SpawnY'] = TAG_Int(self.spawn[1])
            nbt['SpawnZ'] = TAG_Int(self.spawn[2])

        return self.tag


LIVING_ENTITIES = {
    'Chicken': Chicken
}
