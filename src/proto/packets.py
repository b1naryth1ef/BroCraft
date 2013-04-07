from construct import *
from proto.util import *
from encoding import ucs2

import codecs

codecs.register(ucs2)

PACKETS = {
    "\x00": Struct("ping", UBInt32("pid")),
    "\x01": Struct("login", UBInt32("eid"), AlphaString("leveltype"), mode, dimension, difficulty, UBInt8("unused"), UBInt8("maxplayers")),
    "\x02": Struct("handshake", UBInt8("protocol"), AlphaString("username"), AlphaString("host"), UBInt32("port")),
    "\x03": Struct("chat", AlphaString("message")),
    "\xFE": Struct("poll", UBInt8("unused")),
    "\xFF": Struct("dc", AlphaString("message")),
    "\x33": Struct("chunk", SBInt32("x"), SBInt32("z"), Bool("continuous"), UBInt16("primary"), UBInt16("add"), PascalString("data", length_field=UBInt32("length"), encoding="zlib")),
    "\x06": Struct("spawn", SBInt32("x"), SBInt32("y"), SBInt32("z")),
    "\x0D": Struct("location", BFloat64("x"), BFloat64("y"), BFloat64("stance"), BFloat64("z"), BFloat32("rotation"), BFloat32("pitch"), UBInt8("grounded")),
    "\x0B": Struct("position", BFloat64("x"), BFloat64("y"), BFloat64("stance"), BFloat64("z"), UBInt8("grounded")),
    "\x0C": Struct("orientation", BFloat32("rotation"), BFloat32("pitch"), UBInt8("grounded")),
}

PACKET_NAMES = {}

class Packet(object):
    def __init__(self, name=None, struct=None, **kwargs):
        if name is not None: struct = PACKET_NAMES[name]
        self._struct = PACKETS[struct]
        self._id = struct
        self.name = self._struct.name

        self.__dict__.update(kwargs)

    def build(self, **kwargs):
        self.__dict__.update(kwargs)
        return self._id+self._struct.build(self)

    def read(self, data):
        self._data = self._struct.parse(data)
        for k, v in self._data.items():
            self.__dict__[k] = v
        return self

for k, v in PACKETS.items():
    PACKET_NAMES[v.name] = k
