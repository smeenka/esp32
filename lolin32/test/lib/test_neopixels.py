# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
from  neopixels import Neopixels
import utime as time

import logging
logging.setGlobal(logging.DEBUG)
log = logging.getlogger("test")


n = 60
pin = 13
neo = Neopixels(pin,n)
neo.brightness = 50
cindex = 0


# Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.
# return a tuple (r,g,b) 
def  wheel(wheelPos):
    wheelPos = 255 - wheelPos;
    if wheelPos < 85:
       return (255 - wheelPos * 3, 0, wheelPos * 3)
    elif wheelPos < 170:
       wheelPos -= 85;
       return (0, wheelPos * 3, 255 - wheelPos * 3)
    else:
       wheelPos -= 170;
       return (wheelPos * 3, 255 - wheelPos * 3, 0)


for x in range(2):
    for i in range(200): 
        for j in range (n):
            neo.setPixel(j, wheel(i))
        neo.writeBuffer() 
        time.sleep_ms(50)
    log.info("x:%s",x)             
 
print("finished") 