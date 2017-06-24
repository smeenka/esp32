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
from  neoklok import klok
from neostate import neo
import ujson as json

import logging
log = logging.getlogger("webs")
log.setLevel(logging.INFO)

class WebServer:
    def __init__(self,httpserver ):
        log.debug ("Constructor WebServer") 
        self.server = httpserver 

    def modeStation(self):   
        log.debug ("modeStation") 
        server = self.server
        server.resetRouteTable()
        server.onEnd(".css",    self.handleStatic )
        server.onEnd(".js",     self.handleStatic )
        self.server.onExact("/",           self.handleRoot )
        self.server.onExact("/index.html", self.handleRoot )
        self.server.onExact("/aplist.html", self.handleApList )
        self.server.onExact("/ap.html", self.handleAp )
        self.server.onExact("/station.html", self.handleStation )
        self.server.onExact("/kill/os", self.handleKillOs )
        self.server.onExact("/get_ip", self.handleGetIp )
        self.server.onPost("/settings", self.handleStationSettings)
        self.server.onPost("/set_ssid", self.handleSetSSID)
        self.server.onExact("/reset", self.handleReset)

        self.server.onExact("/time/get", self.handleKlokGet)
        self.server.onPost("/time/set", self.handleKlokSync)
        self.server.onStart("/mode/", self.handleMode)
        log.debug ("finished modeStation") 



    def handleRoot(self,request):    
        log.debug("handleRoot")
        if wifi.wlan.isconnected():
            self.handleStation(request)
        else:
            self.handleAp(request)
    
    def handleAp(self,request):
        log.debug("handleAp")
        temp = {}
        temp["#time"] = klok.toString()
        request.sendFile("/html/ap.html",templates = temp)

    def handleStation(self,request):
        log.debug("handleStation")
        temp = {}
        temp["#brightness"] = config.get("brightness")
        temp["#quarters"] = config.get("quarters")
        temp["#offset"] = config.get("offset")
        temp["#bootcount"] = config.get("bootcount")
        temp["#ip"]  = wifi.getIp()
        temp["#status"]= "connected"
        request.sendFile("/html/station.html",templates = temp)
        

    def handleApList(self,request):
        log.debug("handleApList, getting list") 
        aplist = wifi.wlan.scan()
        temp = {}
        temp["#time"] = klok.toString()
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
        request.sendFile("/html/aplist.html",templates = temp)

    def handleSetSSID(self,request):
        log.debug("handleSetSSID") 
        body = request.body
        log.info("body:%s",body)
        fields = body.split('&')
        ssid = fields[0][5:]
        pw   = fields[1][5:]
        log.info("ssid:%s pw:%s",ssid,pw)
        wifi.connect2ap(ssid,pw)
        self.handleStation(request)
 

    def handleStatic(self,request):
        request.sendFile(request.path)

    def handleKillOs(self,request):
        import sys
        sys.exit(0)


    def handleStationSettings(self,request):
        path = request.path
        value = json.loads(request.body)
        v     = int(value["v"]) 
        log.debug ("Path: %s Post:%s value %d",request.path,request.body,v)
        key = request.path[10:]
        config.put(key,v)
        log.debug("put dirty:%s",config.dirty)

        request.sendOk()



    def handleGetIp(self,request):
        log.info("get time %s", wifi.getIp() )
        request.send(200, "application/json",'{"ip","%s"}'%wifi.getIp() )



    def handleReset(self):
        log.debug ("Reset of clock requested")
        import machine
        machine.reset()
    
    def handleMode(self,request):
        mode = request.path[6:]
        neo.setmode(mode,request.params)
        request.send(200, "application/json",'{"ok":true}')


    def handleKlokGet(self,request):
        jsons = klok.getJsonTime()
        log.trace("/time/get: %s", jsons)
        request.send(200, "application/json",jsons )

    def handleKlokSync(self,request):
        path = request.path
        log.debug ("Path: %s Post:%s ",request.path,request.body)
        value = json.loads(request.body)
        klok.hour     = int(value["hour"]) 
        klok.minute     = int(value["minute"]) 
        klok.second     = int(value["second"]) 
        log.debug ("hour: %s minute:%s  second:%s",klok.hour,klok.minute,klok.second)
        request.sendOk()

