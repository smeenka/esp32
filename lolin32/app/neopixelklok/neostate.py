print("== module neostate.py")
from neoklok import klok
import neopixels

import logging
log  = logging.getlogger("neop")
log.setLevel(logging.DEBUG)
import config
import ujson  as json
import asyncio

class Neostate:

    def __init__(self,pin):
        log.info("init Neoklok on pin %d",pin);
        self.neo = neopixels.Neopixels(pin,n=60)

        self.mColor = (10,   255,  10)
        self.sColor = (255,  10,   10)
        self.hColor = (10,    10,   255)
        self.qColor = (10,    10,   10)
        self.neo.brightness = 50
        self.neo.clearBuffer()
        self.stateColor = (150,150,150)
        self.mode = "klok"
        self.params = {}
        self.mupdate = False
        self.cindex = 0

    def setmode(self,mode,params):
        log.info("Set mode to:%s--",mode)
        self.mode = mode
        self.params = params
        self.mupdate = True

    def stateStationConnecting(self):
        self.stateColor = (0,150,0)

    def stateStation(self):
        self.stateColor = (0,0,150)

    def stateAPConnecting(self):
        self.stateColor = (150,0,0)

    def stateOff(self):
        self.stateColor = (0,0,0)

    
    def handleKlok(self):
        neo = self.neo
        if config.dirty:
            neo.offset = config.get("offset")
            q = config.get("quarters")
            if q > 100:
                q = 100
            self.qColor = (q,q,q)
            neo.brightness = config.get("brightness",50)
            if neo.brightness > 100:
                neo.brightness = 100
            config.save()

        local_hour = (klok.hour + config.get("timeoffset",1) ) % 12    
        h = local_hour * 5 + (klok.minute + 6)/12;
        h = int (h % 60)
        neo.clearBuffer()
        neo.setPixel(29,   self.stateColor)
        neo.setPixel(31,   self.stateColor)
        neo.setPixel( 0,  self.qColor);
        neo.setPixel( 15, self.qColor);
        neo.setPixel( 30, self.qColor);
        neo.setPixel( 45, self.qColor);
        neo.addPixel(klok.second,   self.sColor)
        neo.addPixel(klok.minute,   self.mColor)
        neo.addPixel(h,             self.hColor)
        neo.writeBuffer() 

    def handleRainbow(self):
        # cycle through all colours
        self.cindex += 1
        self.cindex %= 256
        # for all pixels
        for i in range ( 0,60):
            windex = (i + self.cindex) % 256 
            self.neo.setPixel(i, self.wheel(windex) )
        self.neo.writeBuffer() 

    def handleColor(self):
        if self.mupdate:
            self.mupdate = False
            r = int(self.params["r"])
            g = int(self.params["g"])
            b = int(self.params["b"])

            # for all pixels
            for i in range ( 0,60):
                self.neo.setPixel(i, (r,g,b) )
            self.neo.writeBuffer() 

    def handlePixel(self):
        if self.mupdate:
            self.mupdate = False
            r = int(self.params["r"])
            g = int(self.params["g"])
            b = int(self.params["b"])
            i = int(self.params["i"])
            self.neo.setPixel(i, (r,g,b) )
            self.neo.writeBuffer() 


    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    # return a tuple (r,g,b) 
    def  wheel(self,wheelPos):
        wheelPos = 255 - wheelPos;
        if wheelPos < 85:
            return (255 - wheelPos * 3, 0, wheelPos * 3)
        elif wheelPos < 170:
            wheelPos -= 85;
            return (0, wheelPos * 3, 255 - wheelPos * 3)
        else:
            wheelPos -= 170;
            return (wheelPos * 3, 255 - wheelPos * 3, 0)



neo = Neostate(13)         
