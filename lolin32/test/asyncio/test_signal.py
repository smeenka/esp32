# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_signal.py")

import logging
log = logging.getlogger("test_signal")
logs = logging.getlogger("sche")
logs.setLevel(logging.INFO)
logging.setGlobal(logging.DEBUG)

import utime as time,sys
import asyncio

from  neopixels import Neopixels

neo = Neopixels(13,4)
neo.brightness = 50

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0


# 4 tasks
def  wait0():
    total = 0
    while True:
        neo.toggleR( 0,80 )
        neo.writeBuffer()
        total += 1
        yield

def  wait1():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        log.info("Task wait1() got signal value:")
        print(result)

def  wait2():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        log.info("Task wait2() got signal value:")
        print(result)

def  wait3():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        log.info("Task wait3() got signal value:")
        print(result)
        if result[1] == 10:
            yield asyncio.KillOs()

def  sender():
    count = 0
    yield
    while True:
        neo.toggleB( 2,80 )
        neo.writeBuffer()
        log.info("Sending signal hello, value: %o ", count)
        yield asyncio.SendSignal("Hello", count)
        yield
        count += 1

now = time.ticks_ms()

# Run them
sched = asyncio.sched
sched.task( wait0() ,period = 1000  )
sched.task( wait1() ,period = 100 )
sched.task( wait2() ,period = 100 )
sched.task( wait3() ,period = 100 )
sched.task( sender(), period = 1000 )

sched.mainloop()
