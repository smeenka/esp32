# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === neopixels ===
# ------------------------------------------------------------
from machine import Pin
from esp import neopixel_write

class Onepixel:
    def __init__(self,pin):
        self.neo = Neopixels(pin,1)

    def rgb(self, c):
        self.neo.setPixel(0,c)
        self.neo.writeBuffer()




class Neopixels:

    def __init__(self,pin, n = 1, offset = 0):
        self.pin = Pin(pin, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
        self.pixnum = n
        self.buf = bytearray(self.pixnum * 3)

        self.brightness = 100
        self.offset     = 0
        self.clearBuffer()

    # add the given color c at given index
    # parameter c: (R,G,B) triple
    # parameter index: int index in the led strip
    def addPixel (self,index, col ):
        index += self.offset
        index %= self.pixnum
        index *= 3
        r, g ,b  = (col)
        self.addColor(index,g)
        self.addColor(index+1,r)
        self.addColor(index+2,b)

    # add the given color c at given index. Only to be used internally
    # parameter c: int,
    # parameter index: int, index in the byte array
    def addColor (self,index, c ):
      
        old = self.buf[index]
        c = c * self.brightness/256
        c += old 
        if c > 255:
            c = 255
        self.buf[index] = int(c)    

    # get the given color c at given index
    # parameter index: int index in the led strip
    # return: an (R,G,B) triple
    def getPixel(self, index):
        index += self.offset
        index %= self.pixnum
        buf = self.buf
        index *= 3
        g = buf[index]   
        r = buf[index+1] 
        b = buf[index+2] 
        return (r,g,b)

    # set the given color c at given index
    # parameter c: (R,G,B) triple
    # parameter index: int index in the led strip
    def setPixel(self, index, col):
        index += self.offset
        index %= self.pixnum
        buf = self.buf
        r, g ,b  = (col)
        r = (r * self.brightness)/256
        g = (g * self.brightness)/256
        b = (b * self.brightness)/256
        index *= 3
        buf[index]   = int(g)
        buf[index+1] = int(r)
        buf[index+2] = int(b)

    def setR(self,index,r):
        i = index*3 + 1
        self.buf[i] = r

    def setG(self,index,g):
        i = index*3 
        self.buf[i] = g

    def setB(self,index,b):
        i = index*3 + 2
        self.buf[i] = b

    def setR(self,index,r):
        i = index*3 + 1
        self.buf[i] = r

    def toggleR(self,index,r):
        i = index*3 + 1
        v = self.buf[i]
        if( v == 0):
            v = r
        else:
            v = 0
        self.buf[i] = v        

    def toggleG(self,index,g):
        i = index*3 
        v = self.buf[i]
        if( v == 0):
            v = g
        else:
            v = 0
        self.buf[i] = v        

    def toggleB(self,index,b):
        i = index*3 + 2
        v = self.buf[i]
        if( v == 0):
            v = b
        else:
            v = 0
        self.buf[i] = v        

    def clearBuffer(self):  
        buf = self.buf
        for i  in range ( len(buf) ):
            buf[i] = 0

    def writeBuffer(self):
        neopixel_write(self.pin, self.buf, True)

       
