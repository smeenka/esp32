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
    status = wifi.apList()
    if status:
        temp = {}
        r = []
        for n in status["networks"]:
            log.debug("ssid:%s, channel:%s RSSI:%s",n[0],n[2],n[3])
            ssid = n[0]
            r.append( (ssid,ssid,n[2],n[3]) )
        temp["@networks"]= r
        temp["#ip"]  = status["ip"]
        temp["#status"]= status["status"]
    else:
        log.warn("Timeout on waiting")  
    request.sendFile("/html/aplist.html",templates = temp)


def handleStatic(request):
    led.value(1)
    request.sendFile(request.path)
    led.value(0)


def handleKillOs(request):
    log.warn("================= handleKillOs")  
    server.shutdown()


import sys
print(sys.path)

server = http_server.HttpServer(sys.path[0] + "/../../web")

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
    yield asyncio.KillOs()

# Run them 
sched = asyncio.sched
sched.task( ledR() , name ="ledR", period = 1000  )
sched.task( server.listen(8080), name = "accept" )
sched.task(kill(),  time2run = 2 * 60 * 1000 )
sched.enablePolling(50) 
sched.mainloop()  

