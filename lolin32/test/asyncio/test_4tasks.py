# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_4tasks.py")

import logging
log = logging.getlogger("test_2tasks")
logm = logging.getlogger("mach")
logm.setLevel(logging.DEBUG)

import utime as time,sys
import asyncio
import utime as time
from  neopixels import Neopixels

neo = Neopixels(13,4)
neo.brightness = 50

import logging
logging.setGlobal(logging.DEBUG)



# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks
def  led0():
    while True:
        neo.setPixel( 0,( 80,80,80) )
        neo.writeBuffer()
        yield
        neo.setPixel( 0,( 80,0,0) )
        neo.writeBuffer()
        yield

def  led1():
    while True:
        neo.toggleR( 1,80 )
        neo.writeBuffer()
        yield
def  led2():
    while True:
        neo.toggleG( 2,80 )
        neo.writeBuffer()
        yield
def  led3():
    while True:
        neo.toggleB( 3,80 )
        neo.writeBuffer()
        yield

def  kill():
    yield
    yield asyncio.KillOs()




now = time.ticks_ms()

# Run them
sched = asyncio.sched
sched.task(led0(),  period = 1000 )
sched.task(led1(),  period = 1000, time2run = 4200)
sched.task(led2(),  period = 1000, time2run = 6400)
sched.task(led3(),  period = 1000, time2run = 8600 )
sched.task(kill(),  time2run = 10000 )

sched.mainloop()
