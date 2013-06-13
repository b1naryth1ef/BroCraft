import logging

log = logging.getLogger("BroCraft")
log.setLevel(logging.DEBUG)

fh = logging.FileHandler("brocraft.log")
fh.setLevel(logging.DEBUG)

format = logging.Formatter("[%(levelname)s] %(asctime)s @ %(lineno)d in %(funcName)s (%(filename)s | %(thread)d): %(message)s")
fh.setFormatter(format)

log.addHandler(fh)
