from construct import *
from collections import namedtuple

class DoubleAdapter(LengthValueAdapter):

    def _encode(self, obj, context):
        return len(obj) / 2, obj

def AlphaString(name):
    return StringAdapter(
        DoubleAdapter(
            Sequence(
                name,
                UBInt16("length"),
                MetaField("data", lambda ctx: ctx["length"] * 2),
            )
        ),
        encoding="ucs2",
    )

# Boolean converter.
def Bool(*args, **kwargs):
    return Flag(*args, default=True, **kwargs)


# Build faces, used during dig and build.
faces = {
    "noop": -1,
    "-y": 0,
    "+y": 1,
    "-z": 2,
    "+z": 3,
    "-x": 4,
    "+x": 5,
}
face = Enum(SBInt8("face"), **faces)

# World dimension.
dimensions = {
    "earth": 0,
    "sky": 1,
    "nether": 255,
}
dimension = Enum(UBInt8("dimension"), **dimensions)

# Difficulty levels
difficulties = {
    "peaceful": 0,
    "easy": 1,
    "normal": 2,
    "hard": 3,
}
difficulty = Enum(UBInt8("difficulty"), **difficulties)

modes = {
    "survival": 0,
    "creative": 1,
    "adventure": 2,
}
mode = Enum(UBInt8("mode"), **modes)

grounded = Struct("grounded", UBInt8("grounded"))
position = Struct(
    "position",
    BFloat64("x"),
    BFloat64("y"),
    BFloat64("stance"),
    BFloat64("z")
)
orientation = Struct("orientation", BFloat32("rotation"), BFloat32("pitch"))

dig_state = Enum(UBInt8("state"), started=0, cancelled=1, stopped=2, checked=3, dropped=4, shooting=5)
animation = Enum(UBInt8("animation"), noop=0, arm=1, hit=2, leave_bed=3, eat=5, unknown=102, crouch=104, uncrouch=105)
action = Enum(UBInt8("action"), crouch=1, uncrouch=2, leave_bed=3, start_sprint=4, stop_sprint=5)

items = Struct(
    "items",
    SBInt16("primary"),
    If(lambda context: context["primary"] >= 0,
        Embed(Struct(
            "item_information",
            UBInt8("count"),
            UBInt16("secondary"),
            Magic("\xff\xff"),
        ))))

entity_type = Enum( #@TODO embed in Entity class
    UBInt8("type"),
    boat=1,
    minecart=10,
    storage_cart=11,
    powered_cart=12,
    tnt=50,
    ender_crystal=51,
    arrow=60,
    snowball=61,
    egg=62,
    thrown_enderpearl=65,
    wither_skull=66,
    # See http://wiki.vg/Entities#Objects
    falling_block=70,
    ender_eye=72,
    thrown_potion=73,
    dragon_egg=74,
    thrown_xp_bottle=75,
    fishing_float=90,
)

status = Enum(
    UBInt8("status"),
    damaged=2,
    killed=3,
    taming=6,
    tamed=7,
    drying=8,
    eating=9,
    sheep_eat=10,
)

window_types = Enum(
    UBInt8("type"),
    chest=0,
    workbench=1,
    furnace=2,
    dispenser=3,
    enchatment_table=4,
    brewing_stand=5,
)

game_states = Enum(
    UBInt8("state"),
    bad_bed=0,
    start_rain=1,
    stop_rain=2,
    mode_change=3,
    run_credits=4,
)

sounds = Enum(
    UBInt32("sid"),
    click2=1000,
    click1=1001,
    bow_fire=1002,
    door_toggle=1003,
    extinguish=1004,
    record_play=1005,
    charge=1007,
    fireball=1008,
    zombie_wood=1010,
    zombie_metal=1011,
    zombie_break=1012,
    wither=1013,
    smoke=2000,
    block_break=2001,
    splash_potion=2002,
    ender_eye=2003,
    blaze=2004,
)

mob_type = Enum( #@TODO move to livingentity
    UBInt8("type"),
    **{
        "Creeper": 50,
        "Skeleton": 51,
        "Spider": 52,
        "GiantZombie": 53,
        "Zombie": 54,
        "Slime": 55,
        "Ghast": 56,
        "ZombiePig": 57,
        "Enderman": 58,
        "CaveSpider": 59,
        "Silverfish": 60,
        "Blaze": 61,
        "MagmaCube": 62,
        "EnderDragon": 63,
        "Wither": 64,
        "Bat": 65,
        "Witch": 66,
        "Pig": 90,
        "Sheep": 91,
        "Cow": 92,
        "Chicken": 93,
        "Squid": 94,
        "Wolf": 95,
        "Mooshroom": 96,
        "Snowman": 97,
        "Ocelot": 98,
        "IronGolem": 99,
        "Villager": 120
    })

Metadata = namedtuple("Metadata", "type value")
metadata_types = ["byte", "short", "int", "float", "string", "slot", "coords"]

# Metadata adaptor.
class MetadataAdapter(Adapter):

    def _decode(self, obj, context):
        d = {}
        for m in obj.data:
            d[m.id.second] = Metadata(metadata_types[m.id.first], m.value)
        return d

    def _encode(self, obj, context):
        c = Container(data=[], terminator=None)
        for k, v in obj.iteritems():
            t, value = v
            d = Container(
                id=Container(first=metadata_types.index(t), second=k),
                value=value,
                peeked=None)
            c.data.append(d)
        if c.data:
            c.data[-1].peeked = 127
        else:
            c.data.append(Container(id=Container(first=0, second=0), value=0,
                peeked=127))
        return c
# Metadata inner container.
metadata_switch = {
    0: UBInt8("value"),
    1: UBInt16("value"),
    2: UBInt32("value"),
    3: BFloat32("value"),
    4: AlphaString("value"),
    5: Struct("slot",
        UBInt16("primary"),
        UBInt8("count"),
        UBInt16("secondary"),
    ),
    6: Struct("coords",
        UBInt32("x"),
        UBInt32("y"),
        UBInt32("z"),
    ),
}
# Possible effects.
# XXX these names aren't really canonized yet
effect = Enum(UBInt8("effect"),
    move_fast=1,
    move_slow=2,
    dig_fast=3,
    dig_slow=4,
    damage_boost=5,
    heal=6,
    harm=7,
    jump=8,
    confusion=9,
    regenerate=10,
    resistance=11,
    fire_resistance=12,
    water_resistance=13,
    invisibility=14,
    blindness=15,
    night_vision=16,
    hunger=17,
    weakness=18,
    poison=19,
    wither=20,
)

# Metadata subconstruct.
metadata = MetadataAdapter(
    Struct("metadata",
        RepeatUntil(lambda obj, context: obj["peeked"] == 0x7f,
            Struct("data",
                BitStruct("id",
                    BitField("first", 3),
                    BitField("second", 5),
                ),
                Switch("value", lambda context: context["id"]["first"],
                    metadata_switch),
                Peek(UBInt8("peeked")),
            ),
        ),
        Const(UBInt8("terminator"), 0x7f),
    ),
)