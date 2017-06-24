# Asyncio cooperative multitasking


[Back to the main page](readme.md)

## For clarity: the original micropython library (https://github.com/micropython/micropython-lib) does contain the official version of the asyncio library.

Thats the official version of asyncio. So please use the official version for your projects.

The version presented here is my version, with no pretentions that it is better or worser than the official version.

That said lets proceed:

The whole cooperative OS is in one file (usyncio) and consists of 460 lines of code!

Whats in here:

* support for timed operations
* support for signaling
* support for IO polling


## Unit tests for asyncio: best way to start!

Modify main.py such that:

	try:
	    print ("Starting application")
	    os.chdir("/test/asyncio")
	    import test
	except Exception as e:
	    print ("Exception:",e)
	except  KeyboardInterrupt:
	    print ("KeyboardInterrupt")

and modify  /test/asyncio/test.py such that the requested test is started.



## Generator 

Each thread in the usyncio is a generator wrapped in a task.

A generator should:
* contain at least one yield statement
* the code up to the first yield is the setup part
* the first yield my not return a value
* While alive the generator should yield

Example of a generator:

	def foo():
	    fooc = 0
	    while fooc < 25:
	        log.info ("I'm foo %d",fooc)
	        fooc += 1
	        yield 

## Tasks

A generator runs within a task, but is default not aware of the task.

A task is created by the scheduler:

	sched = asyncio.sched
	sched.task(foo(), name = "footask", period = 500)
	sched.mainloop()


The task contains the meta data of the generator: 
* interval, timetorun etc.


	tid     	 = Task.taskid   # Task ID
	self.target  = target        #  create coroutine from given generator
	self.params  = None          # Value to send/receive
	self.prio    = prio          # default: 10.   1=very high 100=low
    self.name    = name 		 # name of the task
	self.period  = period        # zero:     run now
	                             # negative: run once
	                             # positive: run at interval
	self.time2run = 			 # the timer tick after which this task should run	

* If period is None and timetorun is None the task will start now, and run without time delay
* If period is 300 and timetorun is None, the task will start in 300 ms and then run every 300 ms
* If period is 300 and timetorun=1000 , the task will start in 
1000 ms and then run every 300 ms
* If period is None and timetorun=1000 , the task will start in 
1000 ms and then run without time delay


## Scheduler

An instance of the scheduler is created in asyncio as a singleton.

There should only be one instance of the scheduler

	import asyncio
	sched = asyncio.sched
	# add tasks ...
	# Optional polling for IO can be enabled by:
	sched.enablePolling(50) 
	# Garbage collection can be enabled by:
	sched.enableGC(100) 
	# last statement:
	sched.mainloop()


## Return class for yield

A yield statement can return a value. This value should be a an instance (or derivate) of base class SystemCall

The SystemCall classes are diveded in next groups:
* task related
	* get a reference to my task
	* get a reference to all tasks
	* kill a task
	* create a task
	* kill the OS

* IO streaming related:
	* register an IO stream: a reader, writer, readerwriter
	* wait for a IO stream

* Signal related:
	* send a signal, with content
	* wait for a signal
	* send a signal and wait for a response






