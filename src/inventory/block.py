
class Block(object): # Inheirt this for stuff that is "special"
    def __init__(self, id, loc):
        self.id = id
        self.loc = loc

    def update(self): pass