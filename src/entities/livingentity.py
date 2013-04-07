from entities.entity import Entity
from pymclevel.nbt import *

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

        self.dim = nbt['Dimension'].value
        self.gametype = nbt['playerGameType'].value
        self.score = nbt['Score'].value
        self.slot = nbt['SelectedItemSlot'].value
        if 'SpawnX' in nbt:
            self.spawn = (nbt['SpawnX'].value, nbt['SpawnY'].value, nbt['SpawnZ'].value)
        else: self.spawn = None
        self.foodLevel = nbt['foodLevel'].value
        self.foodExhaustionLevel = nbt['foodExhaustionLevel'].value
        self.foodSaturationLevel = nbt['foodSaturationLevel'].value
        self.foodTickTimer = nbt['foodTickTimer'].value
        self.xpLevel = nbt['XpLevel'].value
        self.xpPercent = nbt['XpP'].value
        self.xpTotal = nbt['XpTotal'].value
        #@TODO inventories & abilities

        return self

    def saveToNbt(self, nbt):
        LivingEntity.saveToNbt(self, nbt)

        nbt['Dimension'] = TAG_Int(self.dim)
        nbt['playerGameType'] = TAG_Int(self.gametype)
        nbt['Score'] = TAG_Int(self.score)
        nbt['SelectedItemSlot'] = TAG_Int(self.slot)
        if self.spawn:
            nbt['SpawnX'] = TAG_Int(self.spawn[0])
            nbt['SpawnY'] = TAG_Int(self.spawn[1])
            nbt['SpawnZ'] = TAG_Int(self.spawn[2])
        nbt['foodLevel'] = TAG_Int(self.foodLevel)
        nbt['foodExhaustionLevel'] = TAG_Float(self.foodExhaustionLevel)
        nbt['foodSaturationLevel'] = TAG_Float(self.foodSaturationLevel)
        nbt['foodTickTimer'] = TAG_Int(self.foodTickTimer)
        nbt['XpLevel'] = TAG_Int(self.xpLevel)
        nbt['XpP'] = TAG_Float(self.xpPercent)
        nbt['XpTotal'] = TAG_Int(self.xpTotal)

        return self.tag


LIVING_ENTITIES = {
    'Chicken': Chicken
}
