print("Loading module test_pwm ...")
# Created by Anton Smeenk

import uos as os
import sys
import utime as time
import machine
from machine import Pin, PWM

import logging
logging.setGlobal(logging.DEBUG)

led    = machine.Pin(5, mode=machine.Pin.OUT)
print("Switching off blue led")
led.value(0)


pwm0 = PWM( led)      # create PWM object from a pin with blue led
pwm0.freq()             # get current frequency
pwm0.freq(50)           # set frequency
duty = pwm0.duty()             # get current duty cycle

print ("Current duty:",duty)
pwm0.duty()             # get current duty cycle
print ("Setting duty to 200")
pwm0.duty(200)          # set duty cycle


for i in range(200):
    pwm0.duty(i)
    time.sleep_ms(2)

for i in range(200):
    pwm0.duty(200 - i)
    time.sleep_ms(2)

#pwm2 = PWM(Pin(6), freq=500, duty=512) # create and configure in one go