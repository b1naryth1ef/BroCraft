import logging, sys

log = logging.getLogger("BroCraft")
log.setLevel(logging.DEBUG)

fh = logging.FileHandler("brocraft.log")
fh.setLevel(logging.DEBUG)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

fh_format = logging.Formatter("[%(levelname)s] %(asctime)s @ %(lineno)d in %(funcName)s (%(filename)s | %(processName)s > %(thread)d [%(threadName)s]): %(message)s (Logged by %(name)s) ")
sh_format = logging.Formatter("[%(levelname)s] %(asctime)s @ %(lineno)d in %(funcName)s (%(filename)s): %(message)s")

fh.setFormatter(fh_format)
sh.setFormatter(sh_format)

log.addHandler(fh)
log.addHandler(sh)

log.info("Logger Started!")
