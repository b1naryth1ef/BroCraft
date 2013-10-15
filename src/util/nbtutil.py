from pymclevel.nbt import *

key = {
    TAG_Float: float,
    TAG_Short: int,
    TAG_Int: int,
    TAG_Byte: bool,
    TAG_String: str
}

class Tag(object):
    def __init__(self, name, ttype, default=None):
        self.name = name
        self.type = ttype
        self.pytype = key[self.type]
        self.value = None
        self.tag = None

        if hasattr(default, "__call__"):
            self.default = default(self)
        else:
            self.default = default

    def get(self): return self.value
    def set(self, v): self.value = v

    def __get__(self, inst, cls=None):
        if not self.tag: self.tag = inst.tag[self.name]
        if not self.value: self.value = self.tag.value
        return self.get()

    def __set__(self, val):
        self.set(val)

    def __add__(self, other):
        self.set(self.get() + self.pytype(other))

    def __sub__(self, other):
        self.set(self.get() - self.pytype(other))
