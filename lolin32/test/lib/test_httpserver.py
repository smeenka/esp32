# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
print("Loading module test_httpserver ...")
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

print("Switching off green led")
led.value(0)

from  neopixels import Neopixels

neo = Neopixels(13,4)
neo.brightness = 50



def handleRoot(request):
    log.debug("handleRoot, getting list")
    aplist = wifi.wlan.scan()
    temp = {}
    r = []
    for n in aplist:
        ssid    = n[0].decode()
        channel = n[2]
        rssi    = n[3]
        log.debug("ssid:%s, channel:%s RSSI:%s",ssid,channel,rssi)
        r.append( (ssid,ssid,channel,rssi) )
    temp["@networks"]= r
    temp["#ip"]  = wifi.getIp()
    temp["#status"]= "connected"
    yield from request.sendFile("/html/aplist.html",templates = temp)


def handleStatic(request):
    led.value(1)
    yield from request.sendFile(request.path)
    led.value(0)


def handleKillOs(request):
    log.warn("================= handleKillOs")  
    yield
    server.shutdown()


import sys
print(sys.path)

server = http_server.HttpServer("/web/")

# register all routes
server.resetRouteTable()
server.onEnd(".css",          handleStatic )
server.onEnd(".js",           handleStatic )
server.onExact("/",           handleRoot )
server.onExact("/index.html", handleRoot )
server.onExact("/kill",       handleKillOs )


# 2 tasks
def  ledR():
    log.info("Starting ledR")
    yield
    while True:
        neo.toggleR( 1,80 )
        neo.writeBuffer()
        yield

def  kill():
    yield
    log.info("Shut down server!")
    server.shutdown()
    yield asyncio.KillOs()

# Run them 
sched = asyncio.sched
sched.task( ledR() , name ="ledR", period = 1000  )
sched.task( server.listen(80), name = "accept" )
sched.task(kill(),  time2run = 2 * 60 * 1000 )
sched.enablePolling() 
sched.enableGC() 
sched.mainloop()  

