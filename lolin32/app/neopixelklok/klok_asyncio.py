print("== module klok_asyncio.py")
import wifi  
import webserver
import http_server
import logging
import asyncio
import gc
from  neoklok import klok
from  neostate import neo
import config
import ntptime
import utime as time
import ujson as json
import sys

logging.setGlobal(logging.DEBUG)

log  = logging.getlogger("klok")
sche = logging.getlogger("sche")
http = logging.getlogger("http")
webs = logging.getlogger("webs")
neok = logging.getlogger("neok")
sche.setLevel(logging.INFO)
http.setLevel(logging.DEBUG)
webs.setLevel(logging.DEBUG)
log.setLevel(logging.DEBUG)
neok.setLevel(logging.DEBUG)

import sys 
log.info("Current platform: id:%s",sys.platform )

# Two tasks
def heap():
    yield
    while True:
        log.info ("Memory free: %d time:%s" , gc.mem_free() ,  klok.toString() )
        yield

def wlanConnect():
    tick = 10
    yield
    neo.stateStationConnecting()
    wifi.startap('led_klok','12345678')
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
                neo.stateOff()
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
        neo.stateAPConnecting()
    else:
        neo.stateOff()
            

def wlanOff():
    log.info("In about 15 minutes ap will be switched off.")
    yield
    yield asyncio.Wait(1000 * 60 * 15)
    log.info("Switching off ap.")
    wifi.ap.active(False)
    # no yield anymore task will be killed


def klokControl():
    yield
    while True:
        try:
            klok.nextSecond()
        except Exception as e:
            tup = e.args 
            log.warn("in klokControl Exception:%s %s ",e.__class__,tup)
        yield

def neoControl():
    yield
    while True:
        try:
            to = 1000
            if neo.mode == "rainbow":    
                neo.handleRainbow()
                to = 100
            elif neo.mode == "color":    
                neo.handleColor()
                to = 20
            elif neo.mode == "pixel":    
                neo.handlePixel()
                to = 20
            else:
                neo.handleKlok()
            yield asyncio.Wait(to)    
        except Exception as e:
            tup = e.args 
            log.warn("in neoControl Exception:%s %s ",e.__class__,tup)
            yield


http = http_server.HttpServer("web")
port = 80
if sys.platform == "linux": 
    port = 8080

server = webserver.WebServer(http)
server.modeStation()

 
def oncePerDay():
    yield 
    log.info("Checking once per Day")
    while True:
        try:
            hour  = klok.hour
            minu  = klok.minute
            if hour == 3 and minu == 30:
                log.info("Once per day check ntp time")
                yield from wlanConnect()
                yield from wlanOff()
        except Exception as e:
            tup = e.args 
            log.warn("in neoControl Exception:%s %s ",e.__class__,tup)
        yield


log.warn("Config tasks in the scheduler")

sched = asyncio.sched
sched.task(heap(),           name = "heap",     period = 10000)
sched.task(wlanConnect(),    name = "wlan",     period = 1000, time2run = 500)
sched.task(wlanOff(),        name = "wlanOff")
sched.task(klokControl(),    name = "klok",     period = 1000,prio = 5)
sched.task(neoControl(),     name = "neo",      period = 1000)
sched.task(oncePerDay(),     name = "oncePerDay",period = 3600 *1000)
sched.task(http.listen(port),name = "webServer")
sched.enablePolling(50) 
sched.enableGC(100) 
log.info("Loaded class Neopixelklok. Start scheduler")  
sched.mainloop()

