# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_2tasks.py")

import logging
log = logging.getlogger("test_2tasks")
logm = logging.getlogger("mach")
logm.setLevel(logging.INFO)

import utime as time,sys
import asyncio

# Two tasks
def foo():
    fooc = 0
    while fooc < 25:
        log.info ("I'm foo %d",fooc)
        fooc += 1
        yield

def bar():
    barc = 0
    while barc < 25:
        log.info("I'm bar %d",barc)
        barc +=1
        yield
    yield asyncio.KillOs()


# Run them
sched = asyncio.sched
sched.task(bar(), name = "bartask", period = 700)
sched.task(foo(), name = "footask", period = 500)

sched.mainloop()
