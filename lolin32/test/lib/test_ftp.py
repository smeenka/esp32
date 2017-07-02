# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
print("Loading module test_ftp ...")
import asyncftp
import machine
import logging
import asyncio

logging.setGlobal(logging.DEBUG)
log = logging.getlogger("test")
log = logging.getlogger("aftp")
log.setLevel(logging.DEBUG)

led    = machine.Pin(5, mode=machine.Pin.OUT)

# task to check that the OS is still responsive
def  oncePerSec():
    yield
    while True:
        if led.value() == 1:
            led.value(0)
        else:
            led.value(1)    
        yield

DATA_PORT = 1024

# Run them
log.debug("Starting scheduler")
sched = asyncio.sched
sched.task(asyncftp.ftpserver(21,DATA_PORT))
sched.task(oncePerSec(), period = 500)
sched.enablePolling(100) 
sched.enableGC(100) 
log.debug("Starting mainloop")

sched.mainloop(True)
