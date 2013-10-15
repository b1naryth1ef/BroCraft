import struct

class MockData(object):
    def __init__(self, source):
        self.data = list(source)

    def get_multi(self, count, shift=False):
        data = self.data[:count]
        if shift:
            self.lshift(count)
        return data

    def get(self, id=0, shift=False):
        data = self.data[id]
        if shift:
            self.lshift(1)
        return data

    def has(self, id):
        return id < len(self.data)

    def lshift(self, c):
        self.data = self.data[c:]

    def __len__(self):
        return len(self.data)

class Packet(object):
    def __init__(self, data):
        self.__dict__.update(data)

class PacketDef(object):
    def __init__(self, id, name, attrs, client=True):
        self.id = id
        self.name = name
        self.attrs = attrs

        if client:
            CLIENT_PACKETS[id] = self
        else:
            SERVER_PACKETS[id] = self
        MISC_PACKETS[name] = self

    def parse(self, data):
        kw = {
            "id": self.id,
            "name": self.name
        }

        for attr in self.attrs:
            print "Decoding %s as %s" % (attr.name, attr)
            kw[attr.name] = attr._decode(data)
        return Packet(kw)

def decode(data, force_as=None):
    # Attempt to decode header
    length = VarInt._decode(data)
    if not length:
        return None

    # Check if we have enough data, disclude the first length attr
    if len(data) < (length-1):
        return None

    # Decode the packet_id
    packet_id = VarInt._decode(data)

    if force_as:
        return force_as.parse(data)

    return SERVER_PACKETS[hex(packet_id)].parse(data)

class Attrib(object):
    def __init__(self, name, **kwargs):
        self.kwargs = kwargs
        self.name = name

    @classmethod
    def _decode(cls, data):
        raise NotImplementedError("_decode needs an override!")

    @classmethod
    def _encode(cls, data):
        raise NotImplementedError("_encode needs and override!")


class VarInt(Attrib):
    @classmethod
    def _decode(cls, data):
        b = ord(data.get(0))
        i = b & 0x7F

        shift = 7
        index = 0
        while b & 0x80 != 0:
            index += 1
            if not data.has(index):
                return None
            b = ord(data.get(index))
            i |= (b & 0x7F) << shift
            shift += 7
        data.lshift(index+1)
        return i

    @classmethod
    def _encode(cls, data): pass

class String(Attrib):
    @classmethod
    def _decode(cls, data):
        size = VarInt._decode(data)

        if not size:
            return None

        if len(data) < size:
            return None

        result = []
        for index in range(0, size):
            char = data.get(0, shift=True)
            result.append(char)
        return ''.join(result)

    @classmethod
    def _encode(cls, data):
        size = VarInt._encode(len(data))

        result = [size]
        for index in range(0, size):
            result.append(hex(ord(data[index])))
        return ''.join(result)

class JsonString(Attrib):
    @classmethod
    def _decode(cls, data):
        val = String._decode(data)
        return json.loads(val)

    @classmethod
    def _encode(cls, data):
        return String._encode(json.dumps(data))

class StructAttrib(Attrib):
    length = 0
    fmt = ""

    @classmethod
    def _decode(cls, data):
        if len(data) < cls.length:
            return None

        return struct.unpack(cls.fmt, ''.join(data.get_multi(cls.length, shift=True)))[0]

    @classmethod
    def _encode(cls, data):
        return struct.pack(cls.fmt, data)

class Slot(Attrib):
    @classmethod
    def _decode(cls, data):
        # Grab BlockID
        id = UShort._decode(data)
        if id == -1:
            return {"id": -1, "empty": True}

        d = {
            "id": id,
            "empty": False
        }

        d['count'] = Byte._decode(data)
        d['dmg'] = UShort._decode(data)
        d['nbt_len'] = UShort._decode(data)

        if d['nbt_len'] == -1:
            return d

        d['nbt'] = Array._decode(data)
        return d

class Array(Attrib):
    @classmethod
    def _decode(cls, data):
        # Get size
        size = Byte._decode(data)
        result = []
        for i in range(0, size / UInt.length):
            result.append(UInt._decode(daata))
        return result

class UShort(StructAttrib):
    length = 2
    fmt = ">H"

class UInt(StructAttrib):
    length = 4
    fmt = ">L"

class ULong(StructAttrib):
    length = 8
    fmt = ">Q"

class Byte(StructAttrib):
    length = 1
    fmt = ">B"


SERVER_PACKETS = {}
CLIENT_PACKETS = {}
MISC_PACKETS = {}

def getPacket(name):
    return MISC_PACKETS[name]


# Begin Packets
# General
PacketDef(None, "handshake", [VarInt("version"), String("server_addr"), UShort("server_port"), VarInt("state")])

# -> Server
PacketDef("0x0", "login", [String("username")], client=False)

# -> Client
PacketDef("0x0", "keepalive", [UInt("id")])
PacketDef("0x01", "joingame", [UInt("id"), Byte("gamemode"), Byte("dim"), Byte("difficulty"), Byte("max_players")])
PacketDef("0x02", "chatmsg", [JsonString("data")])
PacketDef("0x03", "timeupdate", [ULong("age"), ULong("time")])
PacketDef("0x04", "entity_equipment", [UInt("id"), UShort("slot"), Slot("item")])


if __name__ == "__main__":
    d = MockData("\x0f\x00\x00\x09localhost\x63\xdd\x02")
    print decode(d).__dict__
    print len(d)

