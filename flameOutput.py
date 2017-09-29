import RPi.GPIO as GPIO
import os
import sys
import time
from subprocess import Popen, PIPE

# GPIO pin format
GPIO.setmode(GPIO.BCM)

# pin numbers
ascentPin = 17
exitPin = 18
flamePin = 27

#current state
exitState = True
ascentState = True

GPIO.setup(ascentPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(exitPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(flamePin, GPIO.OUT)

print("exit on pin 18, flame out on pin 27")
while(True):
    exitState = GPIO.input(exitPin)
    ascentState = GPIO.input(ascentPin)
    if(exitState == False):        
        os.system('killall omxplayer.bin')
    elif(ascentState == False):
        GPIO.output(flamePin, GPIO.HIGH)
        time.sleep(2)

    elif(ascentState):
        GPIO.output(flamePin, GPIO.LOW)

    time.sleep(.1)
               
