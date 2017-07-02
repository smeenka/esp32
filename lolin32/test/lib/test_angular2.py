# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
print("Loading module test_angular2 ...")
# Created by Anton Smeenk

import uos as os
import sys
import utime as time
import machine
import network
import usocket as socket
import http_server
import asyncio
import wifi
import logging

log = logging.getlogger("test")
logs = logging.getlogger("sche")
logs.setLevel(logging.TRACE)
logh = logging.getlogger("http")
logh.setLevel(logging.DEBUG)
loge = logging.getlogger("esp")
loge.setLevel(logging.INFO)

logging.setGlobal(logging.DEBUG)

led    = machine.Pin(5, mode=machine.Pin.OUT)

print("Switching off blue led")
led.value(0)

from  neopixels import Neopixels

neo = Neopixels(13,4)
neo.brightness = 50



def handleStatic(request):
    led.value(1)
    request.sendFile(request.path)
    led.value(0)

def handleRoot(request):
    led.value(1)
    request.sendFile("/index.html")
    led.value(0)


def handleKillOs(request):
    server.shutdown()

import sys
print(sys.path)
server = http_server.HttpServer(sys.path[0] + "/../../web/ang")

# register all routes
server.resetRouteTable()
server.onExact("",            handleRoot )
server.onExact("/",            handleRoot )
server.onExact("/index.html", handleStatic )
server.onEnd(".css",          handleStatic )
server.onEnd(".js",           handleStatic )
server.onEnd(".html",         handleStatic )
server.onExact("/kill",       handleKillOs )


# 2 tasks
def  ledR():
    log.info("Starting ledR")
    total = 0
    yield
    while True:
        total += 1
        neo.toggleR( 1,80 )
        neo.writeBuffer()
        yield
        if total > 120:
            log.info("Shut down server!")
            server.shutdown()
            yield asyncio.KillOs()

def  kill():
    yield
    log.info("Shut down server!")
    yield asyncio.KillOs()
# Run them 
sched = asyncio.sched
sched.task( ledR() , name ="ledR", period = 1000  )
sched.task( server.listen(8080), name = "accept" )
sched.task(kill(),  time2run = 2 * 60 * 1000 )
sched.enablePolling(100) 
sched.enableGC(100)
sched.mainloop()  

