# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_gettaskref.py")

import logging
log = logging.getlogger("test_taskref")
logs = logging.getlogger("scheduler")
logs.setLevel(logging.TRACE)

logging.setGlobal(logging.DEBUG)

import utime as time,sys
import asyncio

from  neopixels import Neopixels
neo = Neopixels(13,4)
neo.brightness = 50

ledon = (100,0,100)
ledoff = (0,0,0)

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks
def  led0():
    sos = [(1,1),(1,1),(1,1),   (2,1),(2,1),(2,1),    (1,1),(1,1),(1,10) ]
    yield
    task =  yield asyncio.GetTaskRef()
    log.info ("My task name (of generator led0 is: %s", task.name)
    total = 0
    while True:
        # pick next signal pair
        signal = sos.pop(0)
        sos.append(signal)

        task.period =signal[0] * 100
        neo.setPixel(0,ledon)
        yield

        task.period =signal[1] * 100
        neo.setPixel(0,ledoff)
        yield


def  led1():
    total = 0
    while True:
        neo.toggleR( 1,80 )
        neo.writeBuffer()
        total += 1
        yield
        
def  led2():
    total = 0
    while True:
        neo.toggleB( 2,80 )
        neo.writeBuffer()
        total += 1
        yield
def  led3():
    total = 0
    while True:
        neo.toggleR( 3,80 )
        neo.writeBuffer()
        total += 1
        yield
        log.info("Total of task led3 now: %d"%total)
        if total > 10:
            yield asyncio.KillOs()


# Run them
sched = asyncio.Scheduler()
sched.task(led0(),  period = 1000, time2run = 000)
sched.task(led1(),  period = 1000, time2run = 4200)
sched.task(led2(),  period = 1000, time2run = 6400)
sched.task(led3(),  period = 1000, time2run = 8600 )

log.info("test_taskref")
sched.mainloop() 
