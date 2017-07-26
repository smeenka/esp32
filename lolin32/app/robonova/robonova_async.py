# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === application: neopixel klok  ===
# ------------------------------------------------------------
print("== module robonova_async.py")
import wifi  
import webserver
import http_server
import logging
import asyncio
import gc
import config
import utime as time
import ujson as json
import sys
import robonova_control


logging.setGlobal(logging.DEBUG)

htec  = logging.getlogger("htec")
sche = logging.getlogger("sche")
http = logging.getlogger("http")
webs = logging.getlogger("webs")
log  = logging.getlogger("nova")

sche.setLevel(logging.INFO)
http.setLevel(logging.DEBUG)
webs.setLevel(logging.DEBUG)
htec.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import sys 
log.info("Current platform: id:%s",sys.platform )

# Two tasks
def heap():
    yield
    while True:
        cpuload = (10000 - asyncio.sched.idlecount) / 100
        asyncio.sched.idlecount = 0
        log.info ("Memory free: %d cpu load: %d %% " , gc.mem_free() , cpuload )
        yield

def wlanConnect():
    tick = 10
    yield
    wifi.startap('robonova','12345678')
    yield
    connected = wifi.wlan.isconnected()

    if not connected:
        wifi.connect2ap()
        timeout = 10
        while timeout > 0 and not connected:
            log.info("   Try %d",timeout)
            timeout -= 1
            connected = wifi.wlan.isconnected()
            if connected:
                log.info("Connected to station.")
                #if sys.platform != "linux":
                    #ntptime.settime()
                #    pass
                #now = time.localtime()   
                #klok.sync(now) 
                #klok.checkSummerWinter(now) 
            yield 

    if not connected:
        log.warn("Unable to connect to ssid:%s. Starting AP led_klok ")
    else:
        pass
            

http = http_server.HttpServer("web")
port = 80
if sys.platform == "linux": 
    port = 8080

server = webserver.WebServer(http)

 


log.warn("Config tasks in the scheduler")

DATA_PORT = 1024
sched = asyncio.sched
sched.task(heap(),           name = "heap",     period = 10000)
sched.task(wlanConnect(),    name = "wlan",     period = 1000, time2run = 500)
sched.task(http.listen(port),name = "webServer")
sched.task(robonova_control.servoTask(),name = "servos", period=1000,time2run = 112)

sched.enablePolling(100) 
sched.enableGC(100) 
log.info("All tasks loaded.. Start scheduler")  
sched.mainloop()

