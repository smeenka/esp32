# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === asyncio tests  ===
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_taskwait.py")

import logging
log = logging.getlogger("test")
logs = logging.getlogger("sche")
logs.setLevel(logging.TRACE)
loge = logging.getlogger("esp")
loge.setLevel(logging.INFO)
logging.setGlobal(logging.DEBUG)

import utime as time ,sys
import asyncio

from  neopixels import Neopixels
neo = Neopixels(13,4)
neo.brightness = 50

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks
def  led0():
    total = 0
    yield
    task =  yield asyncio.GetTaskRef()
    tid =  task.tid
    log.info("Task led0() taskid: %d", tid)
    while total < 25:
        neo.toggleR( 0,80 )
        neo.writeBuffer()
        total += 1
        yield
    log.info("Task led0() finished!")

def  led1():
    total = 0
    while True:
        neo.toggleB( 1,80 )
        neo.writeBuffer()
        total += 1
        yield
def  led2():
    total = 0
    while True:
        neo.toggleG( 2,80 )
        neo.writeBuffer()
        total += 1
        yield

def  wait4task0(tid0):
    yield
    result = yield asyncio.WaitTask(tid0)
    log.info("wait4task0: Waiting for task %d to end.Did I wait? : %s",tid0 ,result)
    yield asyncio.KillOs()

now = time.ticks_ms()

# Run them
sched = asyncio.sched
tid0 = sched.task(led0(),  period = 200)
sched.task(led1(),  period = 400, time2run = now +200)
sched.task(led2(),  period = 400, time2run = now +400)
sched.task(wait4task0(tid0)  ,period = 1000,   )

sched.mainloop()
