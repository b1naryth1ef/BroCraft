# -*- coding: utf-8 -*-

COLORS = {
    "black": u"§0",
    "dark_blue": u"§1",
    "dark_green": u"§2",
    "dark_cyan": u"§3",
    "dark_red": u"§4",
    "purple": u"§5",
    "gold": u"§6",
    "gray": u"§7",
    "dark_gray": u"§8",
    "blue": u"§9",
    "green": u"§a",
    "cyan": u"§b",
    "red": u"§c",
    "pink": u"§d",
    "yellow": u"§e",
    "white": u"§f",
    "random": u"§k",
    "bold": u"§l",
    "strike": u"§m",
    "under": u"§n",
    "italic": u"§o",
    "reset": u"§r"
}

def colorize(msg):
    return msg.format(**COLORS)
