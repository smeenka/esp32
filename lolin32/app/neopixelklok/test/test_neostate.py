# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === application test: neopixel klok  ===
# ------------------------------------------------------------
import sys
import utime as time
sys.path.append("../")

from  neoklok import klok
from  neostate import neo

import logging
logging.setGlobal(logging.DEBUG)
log = logging.getlogger("esp") # switch on output for neopixels
log.setLevel(logging.DEBUG)


def commitState():
    neo.neo.setPixel(29,   neo.stateColor)
    neo.neo.setPixel(31,   neo.stateColor)
    neo.neo.writeBuffer() 
    time.sleep(1)


print("stateStationConnecting")
neo.stateStationConnecting()
commitState()

print("stateStation")
neo.stateStation()
commitState()

print("stateAPConnecting")
neo.stateAPConnecting()
commitState()

print("stateOff")
neo.stateOff()
commitState()

print("Rainbow")
for i in range (10):
    neo.handleRainbow()
    time.sleep_ms(100)

print("Klok")
while True:
    klok.nextSecond()
    print(klok.getJsonTime() )
    neo.handleKlok()
    time.sleep(1)
    

