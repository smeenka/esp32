# main.py -- put your code here!
print("Loading module test_lowpower ...")

import uos as os
import sys
import utime as time
import machine
import network


led    = machine.Pin(5, mode=machine.Pin.OUT)

print("Switching off green led")
led.value(0)
time.sleep(5)

print("Switching off WLAN")
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(5)

print("Switching off AP")
ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(5)


print("Forever light sleep")
while True:
    machine.idle()
    time.sleep(5)






ap  = network.WLAN(network.AP_IF)
ap.active(False)


wlan = network.WLAN(network.STA_IF)
#antenna = machine.Pin(16, machine.Pin.OUT, value=0)

if not wlan.active() or not wlan.isconnected():
   wlan.active(True)
   wlan.ifconfig(  ('192.168.2.80', '255.255.255.0', '192.168.2.254', '192.168.2.254') )

   print('connecting to:', ssid)
   wlan.connect(ssid, password)
   while not wlan.isconnected():
      blink(1)

print('network config:', wlan.ifconfig())
blink(5)
try:
    print ("Starting application")
    os.chdir("/test")
    #os.chdir("lib")
    os.chdir('asyncio')
    import test
except Exception as e:
    print ("Exception:",e)
except  KeyboardInterrupt:
    print ("KeyboardInterrupt")

led.value(1)
import uftpserver




