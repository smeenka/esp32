# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
# main.py -- put your code here!
print("Loading module test_lowpower ...")

import uos as os
import sys
import utime as time
import machine
import network
import wifi

led    = machine.Pin(5, mode=machine.Pin.OUT)

print("Switching off blue led")
led.value(1)
time.sleep(5)

print("Switching off WLAN")
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(5)

print("Switching off AP")
ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(5)


print("Sleeping forever")
#while True:
#    machine.idle()


now = time.ticks_ms()
count = 0
while count < 1000:
    machine.idle()
    count += 1
now1 = time.ticks_ms()
diff = now1- now
print("1000 loops in %s ms. Per loop %s ms" %( diff, diff/1000) )
print("Switch on wifi ... " ) 
wifi.connect2ap()





