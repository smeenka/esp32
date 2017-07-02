# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === logging ===
# ------------------------------------------------------------
import utime as time

ERROR    = const(5)
WARNING  = const(4)
INFO     = const(3)
DEBUG    = const(2)
TRACE    = const(1)
NOTSET   = const(0)


class Logger:

    level    = DEBUG
    loggers  = {}
    level2string = ["NOT_SET","TRACE","DEBUG","INFO","WARN","ERROR"]


    def setLevel(self, level):
        if level > ERROR:
            level = ERROR
        self.level = level

    def __init__(self, name):
        self.level = DEBUG
        self.name = name


    def log(self, level, msg, *args):
        if level > ERROR:
            level = ERROR

        if level >= self.level and level >= Logger.level:
            message = msg % args
            now = time.ticks_ms() / 1000
            print( ("%s:%s:%5.3f:%s" )%(Logger.level2string[level], self.name, now,message ))

    def trace(self, msg, *args):
        self.log(TRACE, msg, *args)


    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warn(self, msg, *args):
        self.log(WARNING, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

def setGlobal(level):
    Logger.level = level

def getlogger(name):
    if name in Logger.loggers:
        return Logger.loggers[name]
    l = Logger(name)
    Logger.loggers[name] = l
    return l
