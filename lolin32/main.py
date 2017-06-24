# main.py -- put your code here!
print("Loading module main ...")

import os
import sys
import time
import machine  
import wifi

sys.path.append("/lib")
sys.path.append("/app")

led    = machine.Pin(5, mode=machine.Pin.OUT)

def blink(n):
  for i in range(n):
    led.value(0)
    time.sleep_ms(100)
    led.value(1)
    time.sleep_ms(100)


#wifi.ap.active(False)
wifi.connect2ap()
while not wifi.wlan.isconnected():
    blink(1)
 
print('Connected!! network config:', wifi.wlan.ifconfig())
blink(5)
try:
    print ("Starting application")
    os.chdir("/test/lib")
    #s.chdir('/test/asyncio')
    #import test
    os.chdir("/app/neopixelklok")
    import klok_asyncio

except Exception as e:
    print ("Exception:",e)
except  KeyboardInterrupt:
    print ("KeyboardInterrupt")
   
led.value(1)
import uftpserver




