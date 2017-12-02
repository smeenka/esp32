# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
# main.py -- put your code here!
print("Loading module test_lowpower ...")

import machine
import utime as time


if machine.reset_cause() == 7:
    print ("Wake up due to a sleep timer event. Time is", time.localtime())
    machine.deepsleep(1000)
else:
    rc =  machine.reset_cause()    
    print("Sleeping for 5 seconds...")
    time.sleep(5)
    print("Reboot cause: ", rc)

    from machine import RTC as rtc
    import ntptime 
    import wifi
    wifi.connect2ap()
    print ("DateTime before:",time.localtime())
    ntptime.settime()
    print ("DateTime after ntp time:",time.localtime())

    print(" Deep sleeping for 1 seconds...")
    wifi.off()
    machine.deepsleep(1000)

print(" This line never reached ...")


