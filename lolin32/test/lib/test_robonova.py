# ------------------------------------------------------------
#        Developping with MicroPython in an async way
#
# ------------------------------------------------------------
#                      === library  tests  ===
# ------------------------------------------------------------
# main.py -- put your code here!
print("== module test_robonova ...")

from  hitec_servo_hmi import HitecServo,HitecServoDriver

import logging
import utime as time

log = logging.getlogger("htec")
log = logging.getlogger("test")

driver = HitecServoDriver(2) 
driver.getVoltageAmp()
driver.getVersionId()

zero = HitecServo(driver,0)

shTurn = HitecServo(driver,1)
shLift = HitecServo(driver,2)
elbow = HitecServo(driver,3)
hipSide = HitecServo(driver,4)
hipUp = HitecServo(driver,5)
knee  = HitecServo(driver,6)
enkle = HitecServo(driver,7)
foot  = HitecServo(driver,8)

#driver.setId(7)

servos = [zero,shTurn,shLift,elbow,hipSide,hipUp,knee,enkle,foot]
names  = ["zero","shTurn","shLift","elbow","hipSide","hipUp","knee","enkle","foot"] 
"""
while 1:
	driver.checkStream()
	for servo in servos:
		servo.getPosition()
	time.sleep_ms(500)
"""

for i in range(9):
	name = names[i]
	servo = servos[i]

	driver.checkStream()
	log.info("Servo %s ", name)
	servo.setSpeed(225)
	servo.setPosition(1000)
	servo.getPosition()
	time.sleep(2)
	servo.setPosition(1600)
	servo.getPosition()
	time.sleep(2)
	servo.setPosition(1500)
	servo.getPosition()
	time.sleep(2)

