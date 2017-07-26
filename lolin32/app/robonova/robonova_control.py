print("== loading module robonova_control")

from  hitec_servo_hmi import HitecServo,HitecServoDriver

import logging
import utime as time
import json

log = logging.getlogger("serv")

driverL = HitecServoDriver(2) 
driverL.getVoltageAmp()
driverL.getVersionId()

driverR = HitecServoDriver(1) 
driverR.getVoltageAmp()
driverR.getVersionId()


for i in range(9):
    servo = HitecServo(driverL,i)
    servo.setSpeed(200)

for i in range(9):
    servo = HitecServo(driverR,i)
    servo.setSpeed(200)

driverL.allOn()
driverL.allGain(3)

driverR.allOn()
driverR.allGain(3)


def servoTask():
    yield
    while True:
        driverL.checkStream()            
        for s in driverL.servos:
            if s:
                s.getPosition()
        driverR.checkStream()            
        for s in driverR.servos:
            if s:
                s.getPosition()
        yield 
