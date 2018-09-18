from microbit import *

readDuration = 100
readInterval = 6000

delimiter = ","
serialInterval = 6000

currentTime = 0
readStartTime = 0
lastOutputTime = 0

vPower = 3.3
knownResistor = 100
vDivider = 0

n = 0


def startPower():
    pin7.write_digital(1)


def stopPower():
    pin7.write_digital(0)


def readSensors():
    global vPower, vDivider
    reading = pin10.read_analog()
    if reading <= 3:
        reading = 0
    reading = reading * 3.3
    reading = reading / 1023
    vDivider = reading


def writeToSerial():
    global lastOutputTime
    if currentTime - lastOutputTime > serialInterval:
        print(vDivider)
        lastOutputTime = currentTime


while n < 1:
    uart.init(9600)
    display.off()
    n = 1


while True:
    currentTime = running_time()
    if currentTime - readStartTime >= readInterval:
        readStartTime = currentTime
    elif currentTime - readDuration <= readStartTime:
        startPower()
        sleep(1000)
        readSensors()
#        readSensors()
        sleep(250)
        stopPower()
    else:
        stopPower()

    writeToSerial()
