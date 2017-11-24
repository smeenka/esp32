print ("== Module hitec_servo_hmi")

from machine import UART
import utime as time
import logging
import ujson as json


log = logging.getlogger("htec")

UART2_CONFIG0_REG   = const(0x3FF6E020)
UART_RXD_INV        = const(1 << 19)
UART_TXD_INV        = const(1 << 22)

EEPROM_ID   = const(0x29)  # eeprom addres where the id is stored
#                             p1    p2   function   
READ_EEPROM = const(0xE1)  #  addr  00   read_ eeprom. addr = eeprom addres
WRITE_EEPROM = const(0xE2) #  addr  data  write eeprm (careful!!)
READ_DATA   = const(0xE3)  #  addr  00    read DATA 
WRITE_DATA  = const(0xE4)  #  addr  data  write_DATA
READ_ADC    = const(0xE5)  #  0     0     read ADC position (high,low)
ALL_SERVOS  = const(0xE6)  #  high  low   write postion for all servos
VERSION_ID  = const(0xE7)  #  0     0     B_Version  (version,id)
BATTERY     = const(0xE8)  #  0     0     read  (voltage,current)
POSITION    = const(0xE9)  #  Id    speed set speed and read (pos_high,pos_low)
GAIN        = const(0xEA)  #  0     Gain  can be 1,2 or 3 set gain
ONOFF       = const(0xEB)  #  0     ofoff ofoff = 1 or 0 motor on or off
EXIT        = const(0xEF)  #  0     switch off motor, let servo free run
"""
def invertRxTx():
    u2config0 = ptr32(UART2_CONFIG0_REG) # config 0 reg of uart2
    v = u2config0[0]
    log.info("before config reg %8x", v)
    u2config0[0] = v | UART_RXD_INV | UART_TXD_INV 
    log.info("after config reg %8x", v)
@micropython.asm_thumb
def fun():
    movw(r0, 42)
"""

class HitecServoDriver:

    def __init__(self,port,max = 9):
        log.debug ("HitecServoDriver on port %s", port)
        self.uart = UART(port)                                # init with given baudrate
        self.uart.init(19200, 1, bits=8, parity=None, stop=2) # init with inverted lines
        self.sbuf = bytearray(7)
        self.rbuf = bytearray(7)

        self.sbuf[0]  = 0x80
        self.sbuf[5]  = 0
        self.sbuf[6]  = 0
        self.ri       = 0
        self.V        = 0
        self.I        = 0
        self.version  = 0
        self.id       = 0
        self.servos   = []
        self.positions= []
        for i in range(max):
            self.servos.append(None)
            self.positions.append(0)
        self.allExit() # switch of power to the motors as soon as possible    

    def register(self,servo):
        self.servos[servo.id] = servo   

    def sendCommand(self, command, p1=0,p2=0):
        """send a command """
        uart = self.uart
        buf = self.sbuf
        buf[1]  = command
        buf[2]  = p1
        buf[3]  = p2
        ch      = 0x80 + command + p1 + p2 
        ch     %= 256
        ch      = 256 -  ch
        buf[4]  = ch%256
        uart.write(buf)


    def checkStream(self):
        uart = self.uart
        buf  = self.rbuf
        ri   = self.ri
        while uart.any():
            b = uart.read(1)[0]
            if ri == 0:     # waiting for start of frame
                if b == 0x80:   # start of frame recieved
                    buf[0] = b
                    ri     = 1
            else: 
                buf[ri] = b
                ri     += 1
                if ri >= 7: # complete frame received
                    ri = 0
                    self.parseFrame(buf)



    def parseFrame(self,buf):
        command = buf[1]
        p1      = buf[2]
        r1      = buf[5]
        r2      = buf[6]
        if command == READ_EEPROM:           
            log.info("READ_EEPROM")
        elif command ==READ_DATA:   
            log.info("READ_DATA")
        elif command ==READ_ADC:    
            log.info("READ_ADC")
        elif command ==VERSION_ID:  
            self.version = r1
            self.id      = r2
            log.info("servo version %02x id: %s", r1,r2)
        elif command ==BATTERY:     
            self.I = r1
            self.V = r2
            log.info("battery V: %s I: %s", r2,r1)
        elif command ==POSITION:    
            pos = r1 *256 + r2

            servo = self.getServo(p1)
            if servo:
                servo.pos  = pos 
                self.positions[p1] = pos
                log.debug("servo:%s pos: %s ", p1,pos)
            else:
                log.warn("No servo registerd on id:%s ", p1)  

    def getPosJson(self):
        """Return the positions as an json text array"""
        text = json.dumps(self.positions)
        return text    

        
    def setId(self,newId):
        log.warn("Setting id of servo to %s. ", newId)
        self.sendCommand(WRITE_EEPROM,EEPROM_ID,newId)
        log.warn("Power cycle the servo.")
        

    def readEeprom(self,addr):
        self.sendCommand(READ_EEPROM,addr,0)

        
    def allMove(self, pos):
        h   = pos // 256
        l   = pos % 256
        log.debug("setpos for all to %s",pos)
        self.sendCommand(ALL_SERVOS, h,l)
    
    def getVersionId(self):
        self.sendCommand(VERSION_ID)

    def getVoltageAmp(self):
        self.sendCommand(BATTERY)

    def setPosition(self,index, pos):
        servo = self.getServo(index)
        if servo:
            servo.setPosition(pos)



    def setSpeed(self,index, speed):
        servo = self.getServo(index)
        if servo:
            servo.setSpeed(speed)

    def allGain(self, gain):
        self.sendCommand(GAIN,0, gain)

    def getServo(self,index):
        if 0 <=  index < len(self.servos):
            return self.servos[index]
        else:
            log.warn("Index out of range:%s", index)
            return None

    def allOff(self):
        self.sendCommand(ONOFF,0, 0)

    def allOn(self):
        self.sendCommand(ONOFF,0, 1)

    def allExit(self):
        self.sendCommand(EXIT,0, 0)


class HitecServo:
    def __init__(self,driver, id):
        log.debug ("HitecServo id: %s",id)
        self.driver = driver
        self.speed  = 200
        self.id     = id
        self.pos    = 0
        driver.register(self)


    def setPosition(self,pos = 1500):
        """set position of servo from 800 to 2300. 1500 is mid position.
            """         
        h   = pos // 256
        l   = pos % 256
        log.debug("setpos for id %s to %s",self.id,pos)
        self.driver.sendCommand(self.id, h,l)

    def getPosition(self):
        driver = self.driver
        log.trace("get position for servo %d", self.id)
        self.driver.sendCommand(POSITION,self.id,self.speed)

    def setSpeed(self,speed = 200): 
        self.speed = speed
        self.driver.sendCommand(POSITION,self.id,speed)

    
    def setGain(self,gain):
        self.driver.sendCommand(GAIN,self.id,gain)


    def enable(self, onoff):
        self.driver.sendCommand(ONOFF,self.id, onoff)
        
        
