# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === application: neopixel klok  ===
# ------------------------------------------------------------
print("== module klok_asyncio.py")

import machine
import utime as time

resetCause = machine.reset_cause()    
lowPower   = resetCause == 5


if lowPower:
    print ("Wake up due to a sleep timer event. Run low power")
else:
    print ("Wake up due hard reset or soft reset")
    import ntptime 
    import wifi
    import webserver
    import http_server

print ("Reset cause: %s Time is %s" %(resetCause, time.localtime() ) )


import logging
import asyncio
import gc
from  neoklok import klok
from  neostate import neo
import config
import ntptime
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

sched = asyncio.sched


def heap():
    yield
    while True:
        cpuload = (10000 - asyncio.sched.idlecount) / 100
        cpuidle = asyncio.sched.idlecount / 10
        asyncio.sched.idlecount = 0
        log.info ("Memory free: %d cpu idlecount/sec: %d %% time:%s" , gc.mem_free() , cpuidle,  klok.toString() )
        yield

def wlanConnect():
    tick = 10
    yield
    neo.stateStationConnecting()
    wifi.startap('neoklok','123456789') 
    yield
    connected = wifi.wlan.isconnected()

    if not connected:
        wifi.connect2ap()
        timeout = 10
        while timeout > 0 and not connected:
            log.info("   Try %d",timeout)
            timeout -= 1
            connected = wifi.wlan.isconnected()
            yield
    yield

    if connected:
        neo.stateOff()
        log.info("Connected to station.")
        if sys.platform != "linux":
            ntptime.settime()
        klok.checkSummerWinter() 

    if not connected:
        log.warn("Unable to connect to ssid. Starting AP led_klok ")
        wifi.wlan.disconnect()
        neo.stateAPConnecting()
    else:
        neo.stateOff()
            

def wlanOff():
    log.info("In about 15 minutes wifi will be switched off.")
    yield
    yield
    yield asyncio.Wait(1000 * 60 * 15)
    log.info("Switching off wifi. going to lowpower")
    wifi.ap.active(False)
    wifi.wlan.active(False)    
    machine.deepsleep(1)


def neoControl():
    yield
    task = yield asyncio.GetTaskRef()
    task.period = 1000
    while True:
        try:
            if neo.mode == "rainbow":    
                neo.handleRainbow()
                task.period = 100
            elif neo.mode == "color":    
                neo.handleColor()
                task.period = 20
            elif neo.mode == "pixel":    
                neo.handlePixel()
                task.period = 20
            else:
                neo.handleKlok()
                task.period = 1000
            yield 
        except Exception as e:
            tup = e.args 
            log.warn("in neoControl Exception:%s %s ",e.__class__,tup)
            yield


if not lowPower:
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
            now = time.localtime()
            hour  = now[3]
            minu  = now[4]
            if hour == 3 and minu == 30:
                log.info("Once per day check ntp time")
                import wifi
                yield from wlanConnect()
                yield from wlanOff()
        except Exception as e:
            tup = e.args 
            log.warn("in neoControl Exception:%s %s ",e.__class__,tup)
        yield


log.warn("Config tasks in the scheduler")

sched.task(heap(),           name = "heap",     period = 10000)
sched.task(neoControl(),     name = "neo",      period = 1000)
sched.task(oncePerDay(),     name = "oncePerDay",period = 3600 *1000)
sched.enablePolling(100) 
sched.enableGC(100) 

if not lowPower:
    sched.task(wlanConnect(),    name = "wlan",     period = 1000, time2run = 500)
    sched.task(wlanOff(),        name = "wlanOff")
    sched.task(http.listen(port),name = "webServer")


log.info("Loaded class Neopixelklok. Start scheduler")  
sched.mainloop(True)

