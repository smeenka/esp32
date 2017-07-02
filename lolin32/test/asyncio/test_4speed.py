# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /test/asyncio/test_4speed.py")

import logging
log = logging.getlogger("test_4speed")
logm = logging.getlogger("mach")
logm.setLevel(logging.INFO)

import machine
import sys
import asyncio
import utime as time


# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = [0,0,0,0]
# 4 tasks
def  led0(total):
    yield
    while True:
        #log.info("Ticks: %d  total:%d",time.ticks_ms(),total[0] )
        total[0] += 1
#       leds[0].toggle()
        yield

def  led1(total):
    yield
    while True:
        total[0] += 1
        yield
def  led2(total):
    yield
    while True:
        total[0] += 1
        yield
def  led3(total):
    yield
    while True:
        total[0] += 1
        yield
def  led4(total):
    yield
    while True:
        total[0] += 1
        yield
def  led5(total):
    yield
    while True:
        total[0] += 1
        yield


def  evaluate(total):
    yield
    log.info("Start to evaluate...")
    starttime = time.ticks_ms()
    yield
    endtime = time.ticks_ms()
    t = total[0]
    us = endtime - starttime

    text = "c/s: %f " % (t/ 10)

    log.info("Total millis in 10 second runtime: %f", us / 1000)
    log.info("Total counts:  %d counts /sec: %f ", t, t / 10)
    yield asyncio.KillOs()





# Run them
sched = asyncio.sched

startms = time.ticks_ms()

now = time.ticks_ms()
sched.task(led0 ( total )    , prio = 2, time2run = 1,period = 1000)
sched.task(led1  ( total )  ,  period = 10)
sched.task(led2  ( total )  ,  period = 10)
sched.task(led3 ( total )   ,  period = 5)
sched.task(led4 ( total )   ,  period = 5)
sched.task(led5 ( total )   ,  period = 3)
sched.task(evaluate( total ) , time2run = 1,period = 10000)


millis = time.ticks_ms() - startms
log.info("Total amount of micros needed for creating tasks:  %d ", millis)


sched.mainloop()
