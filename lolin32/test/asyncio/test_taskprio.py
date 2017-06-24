# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_taskprio.py")

import logging

log = logging.getlogger("test_taskprio")
logging.setGlobal(logging.TRACE)

import utime as time
import sys
from  asyncio import Task
from  asyncio import Scheduler



# dummy coroutine
def  dummy():
    yield

taskLate = Task(dummy(), name = "taskLate", prio = 10)
taskEarly = Task(dummy(), name = "taskEarly", prio = 10)
taskMedium5 = Task(dummy(), name = "taskMedium5", prio = 5)
taskMedium15 = Task(dummy(), name = "taskMedium15", prio = 15)

taskLate.time2run  = 1001
taskEarly.time2run  = 110
taskMedium5.time2run  = 500
taskMedium15.time2run  = 500

sched = Scheduler()

def pushonheap(task):
    print ("Pushing task %s  " % task.name   )
    sched.schedule(task)

pushonheap(taskLate)
pushonheap(taskMedium15)
pushonheap(taskMedium5)
pushonheap(taskEarly)

while sched.ready:
    print("Pop from queue: " ,sched.ready.pop(0).name )
