# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_createkilldye.py")

import logging
log = logging.getlogger("test")
logs = logging.getlogger("scheduler")
logs.setLevel(logging.TRACE)
logging.setGlobal(logging.DEBUG)
loge = logging.getlogger("esp")
loge.setLevel(logging.INFO)

import utime as time,sys
import asyncio

from  neopixels import Neopixels

neo = Neopixels(13,4)
neo.brightness = 50
neo.clearBuffer()


# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks

def  led0():
    log.info("Task led0 created!")
    yield
    while True:
        neo.toggleR( 0,80 )
        neo.writeBuffer()
        yield
    log.info("Task led0 dies!")

def  led1():
    yield
    while True:
        neo.toggleG( 1,80 )
        neo.writeBuffer()
        yield
    log.info("Task led1 dies!")

def  led2():
    yield
    while True:
        neo.toggleB( 2,80 )
        neo.writeBuffer()
        yield
    log.info("Task led2 dies!")

def  led3():
    yield
    while True:
        neo.toggleR( 3,80 )
        neo.writeBuffer()
        yield
    log.info("Task led3 dies!")


def  master_of_universe():
    yield
    log.info("Creating task led0. Red led goes flashing fast!")
    tid = yield  asyncio.CreateTask( led0(),  period = 100, prio = 11  )

    log.info("Kill  task led0 with tid %d. Red led stops flashing!",tid)
    yield asyncio.KillTask(tid)

    log.info("Kill the os itself!")
    yield asyncio.KillOs()

    log.info("Task master_of_universe is ready!")





now = time.ticks_ms()

print (now)
# Run them
sched = asyncio.sched
sched.task(led1(),  period = 300,  time2run = 200)
sched.task(led2(),  period = 700, time2run = 300)
sched.task(led3(),  period = 4000, time2run = 4000)
sched.task(master_of_universe(),  period = 4000, time2run = 4000 )

log.info("test creating killing tasks")
sched.mainloop()
