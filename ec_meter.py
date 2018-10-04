# -------------__ Hacking STEM – ec_meter.py – micro:bit __------------
# For use with the Measuring Water Quality to Understand Human Impact 
# lesson plan available from Microsoft Education Workshop at
# http://aka.ms/hackingSTEM
#
#  Overview:
#  This project tests voltage drop through a solution across pin 7 and
#  pin 10.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *

# Cheat to make this approximate the scale on a 5vdc system (Arduino)
SCALE_FACTOR = 2.1044
readDuration = 100
readInterval = 6000

delimiter = ","
serialInterval = 175

currentTime = 0
readStartTime = 0
lastOutputTime = 0

REFERENCE_VOLTAGE = 3.3
knownResistor = 100
vDivider = 0

def startPower():
    pin7.write_digital(1)

def stopPower():
    pin7.write_digital(0)

def readSensors():
    global vDivider
    reading = pin10.read_analog()
    if reading <= 3:
        reading = 0
    reading = reading * REFERENCE_VOLTAGE
    reading = reading / 1023
    vDivider = reading * SCALE_FACTOR


def writeToSerial():
    global lastOutputTime
    if currentTime - lastOutputTime > serialInterval:
        print(vDivider)
        lastOutputTime = currentTime


# setup
uart.init(9600)  # set serial to 9600 baud
display.off()    # turn display off to free pin 10
while True:
    currentTime = running_time()
    if currentTime - readStartTime >= readInterval:
        readStartTime = currentTime
    elif currentTime - readDuration <= readStartTime:
        startPower()
        sleep(250)
        readSensors()
        sleep(250)
        stopPower()
    else:
        stopPower()

    writeToSerial()