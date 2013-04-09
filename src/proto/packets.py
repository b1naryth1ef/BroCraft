from construct import *
from proto.util import *
from encoding import ucs2

import codecs

codecs.register(ucs2)

#Major creds to bravoserver/bravo
PACKETS = {
    0: Struct("ping", UBInt32("pid")),
    1: Struct("login", UBInt32("eid"), AlphaString("leveltype"), mode, dimension, difficulty, UBInt8("unused"), UBInt8("maxplayers")),
    2: Struct("handshake", UBInt8("protocol"), AlphaString("username"), AlphaString("host"), UBInt32("port")),
    3: Struct("chat", AlphaString("message"),),
    4: Struct("time", UBInt64("timestamp"), UBInt64("time")),
    5: Struct("entity-equipment", UBInt32("eid"), UBInt16("slot"), Embed(items)),
    6: Struct("compass", SBInt32("x"), SBInt32("y"), SBInt32("z")),
    7: Struct("use", UBInt32("eid"), UBInt32("target"), UBInt8("button")),
    8: Struct("health", UBInt16("hp"), UBInt16("fp"), BFloat32("saturation")),
    9: Struct("respawn", dimension, difficulty, mode, UBInt16("height"), AlphaString("leveltype")),
    10: Struct("grounded", UBInt8("grounded")),
    13: Struct("location", BFloat64("x"), BFloat64("y"), BFloat64("stance"), BFloat64("z"), BFloat32("yaw"), BFloat32("pitch"), UBInt8("grounded")),
    11: Struct("position", BFloat64("x"), BFloat64("y"), BFloat64("stance"), BFloat64("z"), UBInt8("grounded")),
    12: Struct("orientation", BFloat32("yaw"), BFloat32("pitch"), UBInt8("grounded")),
    14: Struct("digging", dig_state, SBInt32("x"), UBInt8("y"), SBInt32("z"), face),
    15: Struct("build", SBInt32("x"), UBInt8("y"), SBInt32("z"), face, Embed(items), UBInt8("cursorx"), UBInt8("cursory"), UBInt8("cursorz")),
    16: Struct("equip", UBInt16("slot")),
    17: Struct("bed", UBInt32("eid"), UBInt8("unknown"), SBInt32("x"), UBInt8("y"), SBInt32("z")),
    18: Struct("animate", UBInt32("eid"), animation),
    19: Struct("action", UBInt32("eid"), action),
    20: Struct("player", UBInt32("eid"), AlphaString("username"), SBInt32("x"), SBInt32("y"), SBInt32("z"), UBInt8("yaw"), UBInt8("pitch"), SBInt16("item"), metadata),
    21: Struct("pickup", UBInt32("eid"), Embed(items), SBInt32("x"), SBInt32("y"), SBInt32("z"), UBInt8("yaw"), UBInt8("pitch"), UBInt8("roll")),
    22: Struct("collect", UBInt32("eid"), UBInt32("destination")),
    23: Struct("spawn", UBInt32("eid"), entity_type, SBInt32("x"), SBInt32("y"), SBInt32("z"), SBInt32("data"), SBInt16("speedx"), SBInt16("speedy"), SBInt16("speedz")),
    24: Struct("mob", UBInt32("eid"), mob_type, SBInt32("x"), SBInt32("y"), SBInt32("z"), SBInt8("yaw"), SBInt8("pitch"), SBInt8("head_yaw"), SBInt16("vx"), SBInt16("vy"), SBInt16("vz"), metadata),
    25: Struct("painting", UBInt32("eid"), AlphaString("title"), SBInt32("x"), SBInt32("y"), SBInt32("z"), face),
    26: Struct("experience", UBInt32("eid"), SBInt32("x"), SBInt32("y"), SBInt32("z"), UBInt16("quantity")),
    28: Struct("velocity", UBInt32("eid"), SBInt16("dx"), SBInt16("dy"), SBInt16("dz")),
    29: Struct("destroy", UBInt8("count"), MetaArray(lambda context: context["count"], UBInt32("eid"))),
    30: Struct("create", UBInt32("eid")),
    31: Struct("entity-position", UBInt32("eid"), SBInt8("dx"), SBInt8("dy"), SBInt8("dz")),
    32: Struct("entity-orientation", UBInt32("eid"), UBInt8("yaw"), UBInt8("pitch")),
    33: Struct("entity-location", UBInt32("eid"), SBInt8("dx"), SBInt8("dy"), SBInt8("dz"), UBInt8("yaw"), UBInt8("pitch")),
    34: Struct("teleport", UBInt32("eid"), SBInt32("x"), SBInt32("y"), SBInt32("z"), UBInt8("yaw"), UBInt8("pitch")),
    35: Struct("entity-head", UBInt32("eid"), UBInt8("yaw"),),
    38: Struct("status", UBInt32("eid"), status),
    39: Struct("attach", UBInt32("eid"), UBInt32("vid")),
    40: Struct("metadata", UBInt32("eid"), metadata),
    41: Struct("effect", UBInt32("eid"), effect, UBInt8("amount"), UBInt16("duration")),
    42: Struct("uneffect", UBInt32("eid"), effect),
    43: Struct("levelup", BFloat32("current"), UBInt16("level"), UBInt16("total")),
    51: Struct("chunk", SBInt32("x"), SBInt32("z"), Bool("continuous"), UBInt16("primary"), UBInt16("add"), PascalString("data", length_field=UBInt32("length"), encoding="zlib")),
    52: Struct("batch", SBInt32("x"), SBInt32("z"), UBInt16("count"), PascalString("data", length_field=UBInt32("length"))),
    53: Struct("block", SBInt32("x"), UBInt8("y"), SBInt32("z"), UBInt16("type"), UBInt8("meta")),
    54: Struct("block-action", SBInt32("x"), SBInt16("y"), SBInt32("z"), UBInt8("byte1"), UBInt8("byte2"), UBInt16("blockid")),
    55: Struct("block-break-anim", UBInt32("eid"), UBInt32("x"), UBInt32("y"), UBInt32("z"), UBInt8("stage")),
    56: Struct("bulk-chunk", UBInt16("count")), #@TODO
    60: Struct("explosion", BFloat64("x"), BFloat64("y"), BFloat64("z"), BFloat32("radius"), UBInt32("count"), MetaField("blocks", lambda context: context["count"] * 3), BFloat32("motionx"), BFloat32("motiony"), BFloat32("motionz")),
    61: Struct("sound", sounds, SBInt32("x"), UBInt8("y"), SBInt32("z"), UBInt32("data"), Bool("volume-mod")),
    62: Struct("named-sound", AlphaString("name"), UBInt32("x"), UBInt32("y"), UBInt32("z"), BFloat32("volume"), UBInt8("pitch")),
    70: Struct("state", game_states, mode),
    71: Struct("thunderbolt", UBInt32("eid"), UBInt8("gid"), SBInt32("x"), SBInt32("y"), SBInt32("z")),
    100: Struct("window-open", UBInt8("wid"), window_types, AlphaString("title"), UBInt8("slots")),
    101: Struct("window-close", UBInt8("wid")),
    102: Struct("window-action", UBInt8("wid"), UBInt16("slot"), UBInt8("button"), UBInt16("token"), Bool("shift"), Embed(items)),
    103: Struct("window-slot", UBInt8("wid"), UBInt16("slot"), Embed(items)),
    104: Struct("inventory", UBInt8("wid"), UBInt16("length"), MetaArray(lambda context: context["length"], items)),
    105: Struct("window-progress", UBInt8("wid"), UBInt16("bar"), UBInt16("progress")),
    106: Struct("window-token", UBInt8("wid"), UBInt16("token"), Bool("acknowledged")),
    107: Struct("window-creative", UBInt16("slot"), Embed(items)),
    108: Struct("enchant", UBInt8("wid"), UBInt8("enchantment")),
    130: Struct("sign", SBInt32("x"), UBInt16("y"), SBInt32("z"), AlphaString("line1"), AlphaString("line2"), AlphaString("line3"), AlphaString("line4")),
    131: Struct("map", UBInt16("type"), UBInt16("itemid"), PascalString("data", length_field=UBInt8("length"))),
    132: Struct("tile-update", SBInt32("x"), UBInt16("y"), SBInt32("z"), UBInt8("action")),
    200: Struct("statistics", UBInt32("sid"), UBInt8("count")),
    201: Struct("players", AlphaString("username"), Bool("online"), UBInt16("ping")),
    202: Struct("abilities", UBInt8("flags"), UBInt8("fly-speed"), UBInt8("walk-speed")),
    203: Struct("tab", AlphaString("autocomplete")),
    204: Struct("settings", AlphaString("locale"), UBInt8("distance"), UBInt8("chat"), difficulty, Bool("cape")),
    205: Struct("statuses", UBInt8("payload")),
    250: Struct("plugin-message", AlphaString("channel"), UBInt16("length")),
    252: Struct("key-response", UBInt16("shared-len"), UBInt16("token-len")), #@TODO
    253: Struct("key-request", AlphaString("server"), UBInt16("key-len"), UBInt16("token-len")), #@TODO
    254: Struct("poll", UBInt8("unused")),
    255: Struct("dc", AlphaString("message")),
}

PACKET_NAMES = {}

class PacketBase(object): pass

class Packet(PacketBase):
    def __init__(self, name=None, struct=None, **kwargs):
        if name is not None: struct = PACKET_NAMES[name]
        self._struct = PACKETS[struct]
        self._id = struct
        self.name = self._struct.name
        self._pak = None
        self.__dict__.update(kwargs)

    def build(self, **kwargs):
        if self._pak and not kwargs.get("force"): return self._pak
        self.__dict__.update(kwargs)
        self._pak = chr(self._id)+self._struct.build(self)
        return self._pak

    def read(self, data):
        #self._data = self._struct.parse(data)
        for k, v in data.items():
            self.__dict__[k] = v
        return self

    def debug(self): #Imagine B1n fucking something up, and needing a debug function!
        print "DEBUG FOR %s" % self.name
        for k, v in self.__dict__.items():
            print "  %s is %s (%s)" % (k, v, type(v))

class CombPacket(PacketBase):
    def __init__(self, *paks):
        self.paks = paks

    def build(self, **kwargs):
        val = ""
        for i in self.paks:
            val += i.build(**kwargs)

for k, v in PACKETS.items():
    PACKET_NAMES[v.name] = k


packet_stream = Struct(
    "packet_stream",
    OptionalGreedyRange(
        Struct(
            "full_packet",
            UBInt8("header"),
            Switch("payload", lambda context: context["header"], PACKETS),
        ),
    ),
    OptionalGreedyRange(
        UBInt8("leftovers"),
    ),
)

def parse_packets(bytestream):
    container = packet_stream.parse(bytestream)

    l = [(i.header, i.payload) for i in container.full_packet]
    leftovers = "".join(chr(i) for i in container.leftovers)
    return l, leftovers
