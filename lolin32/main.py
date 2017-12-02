# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                === main.py  ===
# ------------------------------------------------------------
print("Loading module main ...")

import os
import sys
import time
import machine  
 
#sys.path.append("/lib")

led    = machine.Pin(5, mode=machine.Pin.OUT)


def blink(n):
  for i in range(n):
    led.value(0)
    time.sleep_ms(100)
    led.value(1)
    time.sleep_ms(100)


#if machine.reset_cause() == machine.SOFT_RESET:
#    print ("Soft reset, doing nothing")
#    print('Connected!! network config:', wifi.wlan.ifconfig())


try:
    print ("Starting application")
    #os.chdir("/test/lib")
    #os.chdir('/test/asyncio')
    #import test
    #os.chdir("/app/rosserver")
    os.chdir("/app/neopixelklok")
    print ("Importing application")
    import klok_asyncio

except Exception as e:
    print ("Exception:",e)
except  KeyboardInterrupt:
    print ("KeyboardInterrupt")
   
led.value(1)
import wifi
if not wifi.wlan.isconnected():
    wifi.connect2ap()
import uftpserver




