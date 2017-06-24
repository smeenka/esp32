# main.py -- put your code here!
print("Loading module main ...")

import os
import sys
import time
import machine  
import network 

sys.path.append("/lib")
sys.path.append("/app")

led    = machine.Pin(5, mode=machine.Pin.OUT)

def blink(n):
  for i in range(n):
    led.value(0)
    time.sleep_ms(100)
    led.value(1)
    time.sleep_ms(100)

blink(2)

ssid="triceratops"
password="g1-gps-doetje"

ap  = network.WLAN(network.AP_IF)
ap.active(False)


wlan = network.WLAN(network.STA_IF) 
#antenna = machine.Pin(16, machine.Pin.OUT, value=0)
wlan.active(False)

if not wlan.active() or not wlan.isconnected():
   wlan.active(True)
   wlan.ifconfig(  ('192.168.2.81', '255.255.255.0', '192.168.2.254', '192.168.2.254') )

   print('connecting to:', ssid)
   wlan.connect(ssid, password)
   while not wlan.isconnected():
      blink(1)
 
print('network config:', wlan.ifconfig())
blink(5)
try:
    print ("Starting application")
    os.chdir("/test/lib")
    #s.chdir('/test/asyncio')
    #import test
    #os.chdir("/app/neopixelklok")
    #blink(5)
    #import klok_asyncio

except Exception as e:
    print ("Exception:",e)
except  KeyboardInterrupt:
    print ("KeyboardInterrupt")
   
led.value(1)
import uftpserver




