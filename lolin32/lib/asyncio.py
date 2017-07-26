# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === Scheduler ===
# ------------------------------------------------------------
import logging
import utime as time
import uselect as select 
import machine
import gc

log = logging.getlogger("sche")
 

class Scheduler(object):
    def __init__(self):
        self.ready   = []
        self.taskmap = {}
        self.taskStartTime = 0

        # Tasks waiting for other tasks to exit
        self.exit_waiting = {}
        self.signal_waiting = {}
        self.idlecount = 0

        # I/O waiting
        self.io_waiting_task  = {} # key task, value streamobj
        self.poll = select.poll()   # create instance of poll class
        self.usb = None



    def task(self,target,name = "", prio = 10, period = 0, time2run = 0):
        """ Create new task from target. Return taskid form new task
            Target must be of type generator, prio 1 is higgest prio,
            period is time in ms, timer2run is starttime in ms
        """
        newtask = Task(target,name,prio,period, time2run)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)


        return newtask.tid

    def exit(self,task):
        log.debug("Task %s terminated" , task.name)
        self.taskmap.pop(task.tid,None)
        # pop waiting list for this task (or empty list if none is waiting)
        waiting = self.exit_waiting.pop(task.tid,[])
        for task in waiting:
            self.schedule(task)
        # remove task from IO waiting list
        file = self.io_waiting_task.pop(task,None)
        if file:
            log.debug("Deleting stream from waiting list  ")                
            self.poll.unregister(file)
            file.close()
    

    def waitforexit(self,task,waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid,[]).append(task)
            return True
        else:
            return False

    def wait4signal(self, task, signal):
        log.debug ("wait4signal  %s " ,signal )
        self.signal_waiting.setdefault(signal,[]).append(task)

    def wait4signals(self, task, signals):
        for signal in signals:
            self.wait4signal(task,signal)


    def sendsignal(self,signal,value = None):
        # pop waiting list for this signal (or empty list if none is waiting)
        log.debug ("sendsignal  %s value:%s " ,signal ,value)
        waiting = self.signal_waiting.pop(signal,[])
        now = time.ticks_ms()
        for task in waiting:
            task.params = (signal,value)
            task.time2run = now 
            self.schedule(task)

    # I/O waiting
    def registerUsb(self,task,usb):
        self.usb = usb
        self.io_waiting[usb] = task

    def _pollingCoroutine(self):
        while True:
            yield
            readylist= self.poll.poll(0)

            for tuples in readylist:
                file = tuples[0]
                for task,f in self.io_waiting_task.items():
                    if f == file:
                        #log.info("Scheduling task id %s" % task.name)
                        self.schedule(task)
                        break


            if self.usb and self.usb.any():
                readyTask = self.io_waiting[self.usb]
                if readyTask:
                    self.schedule(readyTask)

    def  _garbage(self):
        log.info("Starting garbage collect")
        yield
        while True:
            gc.collect()
            yield


    def schedule(self,task):
        if task not in self.ready:
            self.ready.append(task)
        self.readySiftDown()

    def enablePolling(self, periodms= 100):
        polling = Task(self._pollingCoroutine(), name = "IOPoller",period = periodms , prio = 5)
        self.schedule(polling)

    def enableGC(self, periodms= 100):
        gc = Task(self._garbage(), name = "Garbage",period = periodms , prio = 5)
        self.schedule(gc)


    def mainloop(self, stopOnError = False):
        now = 0
        while True:
            if time.ticks_ms() <= now:
                continue

            if self.ready:
                # fix current millis, before start of task
                now = time.ticks_ms()
                task = self.ready[0]     # peek queue
                if task.time2run <= now:
                    if task.period > 0:
                        task.time2run += task.period 
                    else:
                        task.time2run = now   
                    #log.info ("Memory free: %d" , gc.mem_free() )

                    self.ready.pop( 0 )  # remove item for queue
#                    rq = "queue: "
#                    for t in self.ready:
#                        rq = "%s %s %d" % (rq,t.name,t.tid)
#                    log.info (rq)

                    log.trace ("Running task %s , %d , %d" ,task.name ,task.tid,task.time2run)
                    result = None
                    try:
                        result = task.run()
                    except StopIteration: 
                        self.exit(task)
                        continue  # do not reschedule current task
                    except Exception  as e:
                        tup = e.args
                        log.warn("Task %s: Exception: %s %s ",task.name, e.__class__,tup)   
                        if stopOnError:
                            raise e

                    if result:
                        if isinstance (result,Streamer):
                            mask = select.POLLIN    
                            if isinstance(result, StreamWait):
                                # task will be rescheduled by the poller
                                 continue  # do not reschedule current task

                            elif isinstance(result, StreamReader):
                                pass
                            elif isinstance(result, StreamWriter):
                                mask = select.POLLOUT
                                
                            elif isinstance(result, StreamReaderWriter):
                                mask |= select.POLLOUT
                            # task will be rescheduled by the poller
                            fd = result.fd 
                            log.debug("Registered stream")
                            self.poll.register(fd, mask)
                            self.io_waiting_task[task] = fd 

                        if isinstance (result,Tasker):
                            # All taskers will be rescheduled!
                            if isinstance(result, GetTaskRef):
                                 task.params  = task

                            elif isinstance(result, Wait):
                                 task.time2run -= task.period
                                 task.time2run += result.timeout 

                            elif isinstance(result, AddTask):
                                task = result.task
                                self.taskmap[task.tid] = task
                                self.schedule(task)

                            elif isinstance(result, WaitTask):
                                 result = self.waitforexit(task,result.tid)
                                 task.params  = result
                                 # If waiting for a non-existent task,
                                 # reschedule current task now
                                 if  result:
                                     continue

                            elif isinstance(result, CreateTask):
                                 log.debug(  "CreateTask called by: %s ", task.name)
                                 tid = self.task(result.target, result.name,result.prio,result.period, result.time2run)
                                 task.params  = tid

                            elif isinstance(result, KillTask):
                                log.debug(  "KillTask called by:%s ", task.name)
                                kill = self.taskmap.pop(result.tid,None)
                                if kill:
                                    kill.target.close()
                                    task.params  = True
                                else:
                                    task.params  = False


                            elif isinstance(result, GetTaskDict):
                                 task.params  = self.taskmap


                            elif isinstance(result, KillOs):
                                for tid in self.taskmap:
                                    kill = self.taskmap.pop(tid,None)
                                    if kill:
                                        log.debug  ("Killing task %s", kill.name)
                                        kill.target.close()
                                log.info  ("Goodbye cruel world, I am dying")
                                return


                        if isinstance (result,Signaler):
                            to = result.timeout
                            if isinstance(result, SendSignal):
                                 self.sendsignal(result.signal, result.value)
                                 # reschedule current task

                            elif isinstance(result, SendWaitSignal):
                                 self.sendsignal(result.signal, result.value )
                                 self.wait4signal(task,result.signal)

                            elif isinstance(result, Wait4Signal):
                                 self.wait4signal(task,result.signal)

                            elif isinstance(result, Wait4Signals):
                                 self.wait4signals(task,result.signals)


                            if  to > 0:
                                ## reschedule task for timeout
                                task.time2run = now + to
                            else:   
                                continue  # do not reschedule current task

                    self.schedule(task)            
                else:
                    self.idlecount += 1
                    machine.idle()
            else:
                self.idlecount += 1
                machine.idle()

       

    """ priority queue invariant quard
    Prioriy queue is a queue for which a[k] < a[k+1]  for all k
    Popping the first element from the queue will maintian this invariant.
    When pushing an element at the end of the array, the invariant must be guarded.
    This is done by comparing each 2 elements and swapping element if needed
    """
    def  readySiftDown(self):
        heap = self.ready
        hlen = len(heap)

        if hlen < 2:
            return

        posLeft = hlen  - 2
        # Follow the path to the root, shifting 2 neigbours if in wrong order
        # Stop at the monent no shift is needed
        # newtask fits.
        while posLeft >= 0 :
            posRight = posLeft + 1
            left  = heap[posLeft]
            right =heap[posRight]
            if  right.__lt__( left):
                heap[posLeft]   = right
                heap[posRight] = left
            else:
                break
            posLeft = posLeft - 1





# each yield should return an instance (or derivate) of next base class
class SystemCall(object):
    pass

# Task and OS related tasks
class Tasker(SystemCall):
    pass

# Return a task its own task reference
class GetTaskRef(Tasker):
    pass

class AddTask(Tasker):
    def __init__(self,task):
        self.task = task


# Return the PyOs task dictionary
# Be carefull with that axe Jane!
class GetTaskDict(Tasker):
    pass

# Kill a task
class KillTask(Tasker):
    def __init__(self,tid):
        self.tid = tid

# Wait for a task to exit
class WaitTask(Tasker):
    def __init__(self,tid):
        self.tid = tid



# Kill the Os scheduler. Usefull for testing
class KillOs(Tasker):
    pass

# Create a new task, calling coroutine gets a tid of the created task
class CreateTask(Tasker):
    def __init__(self,target, name = "", prio = 10, period = 0, time2run = 0):
        self.target     = target
        self.name       = name
        self.prio       = prio
        self.time2run   = time2run
        self.period     = period

# let the current task wait for the given ms
class Wait(Tasker):
    def __init__(self,timeout = 0):
        self.timeout = timeout

# Stream related classes
class Streamer(SystemCall):
    pass

class StreamReader(Streamer):
    def __init__(self,fd):
        self.fd = fd

class StreamWriter(Streamer):
    def __init__(self,fd):
        self.fd = fd

class StreamReaderWriter(Streamer):
    def __init__(self,fd):
        self.fd = fd


class StreamWait(Streamer):
    pass







# Wait for reading
class IOWait(SystemCall):
    def __init__(self,fd):
        self.fd = fd


# Signal related tasks
class Signaler(SystemCall):
    pass


# Wait for a list of signals. Do not reschedule current task
class Wait4Signals(Signaler):
    def __init__(self,signals):
        self.signals = signals
        self.timeout = 0

# Wait for a signal. Do reschedule current task with a given timout
class Wait4Signal(Signaler):
    def __init__(self,signal,timeout = 0):
        self.signal = signal
        self.timeout = timeout

# send a signal. Reschedule current task to run after 1 ms wait
class SendSignal(Signaler):
    def __init__(self,signal,value = None,timeout = 1):
        self.signal = signal
        self.value = value
        self.timeout = timeout

class SendWaitSignal(Signaler):
    def __init__(self,signal,value = None, timeout = 0):
        self.signal = signal
        self.value = value
        self.timeout = timeout



class Task(object):
    taskid = 0
    def __init__(self,target, name = "", prio = 10, period = 0, time2run = 0):
        """ Create task and run its target to the first yield
            Target must be a generator object
        """
        Task.taskid += 1
        self.tid     = Task.taskid   # Task ID
        self.target  = target         #  create coroutine from given generator
        self.params  = None        # Value to send/receive
        self.prio    = prio
        if name == "":
            self.name = "task_%d" % self.tid
        else:
            self.name = name
        self.period   = period       # zero:     run now
                                     # negative: run once
                                     # positive: run at interval
        self.time2run = time.ticks_ms();
        if time2run>0:
            self.time2run += time2run
        else:    
            self.time2run += period
        log.debug("Created task %s %d ", self.name,self.tid)
        self.target.send(None)

    def run(self):
        """ Run a task until it hits the next yield statement """
#        log.trace(" run task %s ", self.name)
        return self.target.send(self.params)

    def __lt__(self,other):
        """ compare other task with this one. If  this task is smaller than the other one, return True else False """
        if self. time2run < other.time2run:
            return True;
        if   self.prio < other.prio:
            if self. time2run == other.time2run:
                return  True
        return False
    

# An exception class that is never raised by any code anywhere
class NeverMatch(Exception):
    pass
    
#create instance of scheduler, so that it is globally visible for all programs
sched = Scheduler()
