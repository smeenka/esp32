# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
# main.py -- put your code here!
print("== module test_HitecServo ...")

from  hitec_servo_hmi import HitecServo,HitecServoDriver

import logging
import utime as time

log = logging.getlogger("htec")
log = logging.getlogger("test")

# creat a driver connected to uart2
driver = HitecServoDriver(2, max = 4) 
driver.getVoltageAmp()
driver.getVersionId()
#must be called othwer wise some servos work, other not
driver.allGain(3)

#assumed is that the servos already did get an id
shoulder= HitecServo(driver,1)
upper   = HitecServo(driver,2)
elbow   = HitecServo(driver,3)
zero    = HitecServo(driver,0)

# use only when only one servo is connected. Do a power cycle to make it effectve.
# dont forget to comment the line again after use
#driver.setId(7)


def nextStep(speed, posSh, posUp, posElbow):
	driver.checkStream()
	for servo in driver.servos:
		servo.getPosition()	
		servo.setSpeed(speed)
	shoulder.setPosition(posSh)
	upper.setPosition(posUp)
	elbow.setPosition(posElbow)
	zero.setPosition(posElbow)
	time.sleep_ms(3000)

while True:
	nextStep(200,600,1000,1000)
	nextStep(250,2500,2000,2500)
	nextStep(200,2000,2500,2000)
	nextStep(220,1000,1000,1000)
	nextStep(200,600,1500,1500)
