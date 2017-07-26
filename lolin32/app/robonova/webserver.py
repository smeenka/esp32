# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === application: neopixel klok  ===
# ------------------------------------------------------------
print("== module webserver.py")
### Author: Anton Smeenk
### Description: HTTP Server able to handle routes and parameters
import usocket as socket
import gc
import utime as time
import array
import sys
import wifi
import config
import ujson as json
from  robonova_control import driverL, driverR

import logging
log = logging.getlogger("webs")
log.setLevel(logging.INFO)

class WebServer:
    def __init__(self,httpserver ):
        log.debug ("Constructor WebServer") 
        self.server = httpserver 

        server = self.server
        server.resetRouteTable()
        server.onEnd(".css",    self.handleStatic )
        server.onEnd(".js",     self.handleStatic )
        self.server.onExact("/servos/positions", self.handleGetPos)

        self.server.onExact("/",           self.handleRoot )
        self.server.onExact("/index.html", self.handleRoot )
        self.server.onExact("/aplist.html", self.handleApList )
        self.server.onExact("/ap.html", self.handleAp )
        self.server.onExact("/station.html", self.handleStation )
        self.server.onExact("/reset", self.handleReset)

        self.server.onExact("/kill/os", self.handleKillOs )
        self.server.onExact("/get_ip", self.handleGetIp )

        self.server.onPost ("/servos/position", self.handleSetPos)
        self.server.onPost ("/servos/speed", self.handleSetSpeed)
        self.server.onPost ("/servos/gain", self.handleSetGain)
        self.server.onPost ("/servos/id", self.handleSetId)
        self.server.onPost ("/servos/all", self.handleSetAll)
        self.server.onPost ("/set_ssid", self.handleSetSSID)

        log.debug ("finished modeStation") 



    def handleRoot(self,request):    
        log.debug("handleRoot")
        if wifi.wlan.isconnected():
            yield from self.handleStation(request)
        else:
            yield from self.handleAp(request)
    
    def handleAp(self,request):
        log.debug("handleAp")
        temp = {}
        temp["#time"] = "not implemented yet"
        yield from request.sendFile("/html/ap.html",templates = temp)

    def handleStation(self,request):
        temp = {}
        temp["#brightness"] = config.get("brightness")
        temp["#quarters"] = config.get("quarters")
        temp["#offset"] = config.get("offset")
        temp["#bootcount"] = config.get("bootcount")
        temp["#ip"]  = wifi.getIp()
        temp["#status"]= "connected"
        yield from request.sendFile("/html/station.html",templates = temp)
        

    def handleApList(self,request):
        log.debug("handleApList, getting list") 
        aplist = wifi.wlan.scan()
        temp = {}
        temp["#time"] = "tbd"
        r = []
        for n in aplist:
            ssid    = n[0].decode()
            channel = n[2]
            rssi    = n[3]
            log.debug("ssid:%s, channel:%s RSSI:%s",ssid,channel,rssi)
            if rssi > -80:
                r.append( (ssid,ssid,channel,rssi) )
        temp["@networks"]= r
        temp["#ip"]  = wifi.getIp()
        temp["#status"]= "connected"
        yield from request.sendFile("/html/aplist.html",templates = temp)

    def handleSetSSID(self,request):
        log.debug("handleSetSSID") 
        body = request.body
        log.info("body:%s",body)
        fields = body.split('&')
        ssid = fields[0][5:]
        pw   = fields[1][5:]
        log.info("ssid:%s pw:%s",ssid,pw)
        wifi.connect2ap(ssid,pw)
        yield from self.handleStation(request)
 

    def handleStatic(self,request):
        yield from request.sendFile(request.path)

    def handleKillOs(self,request):
        import sys
        yield
        sys.exit(0)


    def handleStationSettings(self,request):
        path = request.path
        value = json.loads(request.body)
        v     = int(value["v"]) 
        log.debug ("Path: %s Post:%s value %d",request.path,request.body,v)
        key = request.path[10:]
        config.put(key,v)
        log.debug("put dirty:%s",config.dirty)

        yield from request.sendOk()

    def handleSetPos(self,request):
        path = request.path
        value = json.loads(request.body)
        pos    = int(value["pos"]) 
        id     = int(value["id"]) 
        group     = value["group"]
        log.debug ("Set position for group:%s id %d to %d ",group,id,pos)
        if "L" in group:
            driverL.setPosition(id,pos)
        if "R" in group:
            driverR.setPosition(id,pos)
        yield from request.sendOk()

    def handleSetAll(self,request):
        path = request.path
        value = json.loads(request.body)
        pos    = int(value["pos"]) 
        group     = value["group"]
        log.debug ("Group: %a Set position all to %d ",group,pos)
        if "L" in group:
            driverL.allMove(pos)
        if "R" in group:
            driverR.allMove(pos)
        yield from request.sendOk()

    def handleSetSpeed(self,request):
        path = request.path
        value = json.loads(request.body)
        log.debug(request.body)
        id        = int(value["id"]) 
        speed     = int(value["speed"]) 
        group     = value["group"]
        log.debug ("Set speed for group: %sid %d to %d ",group,id,speed)
        if "L" in group:
            driverL.setSpeed(id,speed)
        if "R" in group:
            driverR.setSpeed(id,speed)
        yield from request.sendOk()

    def handleSetGain(self,request):
        path = request.path
        value = json.loads(request.body)
        log.debug(request.body)
        gain     = int(value["gain"]) 
        group     = value["group"]
        log.debug ("Set gain for group: %s to %d ",group,gain)
        if "L" in group:
            driverL.allGain(gain)
        if "R" in group:
            driverR.allGain(gain)
        yield from request.sendOk()


    def handleSetId(self,request):
        path  = request.path
        value = json.loads(request.body)
        newid     = int(value["id"]) 
        group     = value["group"]
        if "L" in group:
            log.debug ("Set newid for group Left to  %d",newid)
            driverL.setId(newid)
        if "R" in group:
            log.debug ("Set newid for group Right to  %d",newid)
            driverR.setId(newid)
        yield from request.sendOk()



    def handleGetIp(self,request):
        log.info("get time %s", wifi.getIp() )
        yield from request.send(200, "application/json",'{"ip","%s"}'%wifi.getIp() )

    def handleGetPos(self,request):
        jsons = driverL.getPosJson()
        yield from request.send(200, "application/json",jsons )


    def handleReset(self):
        log.debug ("Reset of clock requested")
        import machine
        yield
        machine.reset()
    



