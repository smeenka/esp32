import sys
sys.path.append("../")

import webserver
import http_server
import logging
import utime as time
import wifi
import asyncio
from  neoklok import klok
import machine

logging.setGlobal(logging.DEBUG)

log  = logging.getlogger("test")
log.setLevel(logging.DEBUG)
http = logging.getlogger("http")
webs = logging.getlogger("webs")
http.setLevel(logging.DEBUG)
webs.setLevel(logging.DEBUG)


 

log.info ("WebserverTest") 

import sys
print(sys.path)

https = http_server.HttpServer(sys.path[0] + "/../web")
server = webserver.WebServer(https)
server.modeStation()


# 2 tasks
def  ledR():
    log.info("Starting ledR")
    led    = machine.Pin(5, mode=machine.Pin.OUT)  
    total = 0
    yield
    while True:
        total += 1
        if led.value() == 1:
            led.value(0)
        else:
            led.value(1)    
        yield

# 2 tasks
def  taskKlok():
    log.info("Starting Klok")
    total = 0
    yield
    while True:
        total += 1
        klok.nextSecond()
        yield

def  kill():
    yield
    https.shutdown()
    yield asyncio.KillOs()

# Run them
sched = asyncio.sched
sched.task( ledR() , name ="ledR", period = 1000  )
sched.task( taskKlok() , name ="klok", period = 1000  )
sched.task( https.listen(8080), name = "accept" )
sched.task(kill(),  time2run = 2 * 60 * 1000 )
sched.enablePolling(50) 
sched.enableGC(100) 
sched.mainloop()  