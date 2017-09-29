import RPi.GPIO as GPIO
import os
import sys
import time
from subprocess import Popen, PIPE

# GPIO pin format
GPIO.setmode(GPIO.BCM)

ascentPin = 17
descentPin = 4

GPIO.setup(ascentPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(descentPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

a1 = ("/home/pi/py/wow/videos/A1.mp4")
a2 = ("/home/pi/py/wow/videos/A2.mp4")
a3 = ("/home/pi/py/wow/videos/A3.mp4")
d1 = ("/home/pi/py/wow/videos/D1.mp4")
d2 = ("/home/pi/py/wow/videos/D2.mp4")
d3 = ("/home/pi/py/wow/videos/D3.mp4")
slideshow = ("/home/pi/py/wow/videos/slideshow.mp4")

ascentState = True
descentState = True
lastAscentState = True
lastDescentState = True

height = 0
mode = 0
timeToPause = 0
timeToHang = 0
omxc = Popen(['omxplayer', '-b', '--loop', slideshow], stdin=PIPE, stdout=PIPE, close_fds=True)

playTimeA = [32, 20, 60] #[30, 19, 60] 
playTimeD = [10, 23, 32] #[10, 22, 31]

def goingUp():
    global height
    global mode
    global omxc
    global timeToPause
    
    print("going up")
    os.system('killall omxplayer.bin')
    if(height == 0):
        omxc = Popen(['omxplayer', '-b', a1], stdin=PIPE, stdout=PIPE, close_fds=True)
    elif(height == 1):
        omxc = Popen(['omxplayer', '-b', a2], stdin=PIPE, stdout=PIPE, close_fds=True)
    elif(height == 2 or height == 3):
        omxc = Popen(['omxplayer', '-b', a3], stdin=PIPE, stdout=PIPE, close_fds=True)

    timeToPause = time.time() + playTimeA[height]
    mode = 1 # playing, waiting until time to pause
    height = height + 1
    if(height > 3):
        height = 3

def goingDown():
    global height
    global mode
    global omxc
    global timeToPause
    
    print("going down")
    os.system('killall omxplayer.bin')
    if(height == 3):
        omxc = Popen(['omxplayer', '-b', d3], stdin=PIPE, stdout=PIPE, close_fds=True)
    elif(height == 2):
        omxc = Popen(['omxplayer', '-b', d2], stdin=PIPE, stdout=PIPE, close_fds=True)
    if(height == 1):
        omxc = Popen(['omxplayer', '-b', d1], stdin=PIPE, stdout=PIPE, close_fds=True)

    timeToPause = time.time() + playTimeD[height-1]
    mode = 1 # playing, waiting until time to pause
    height = 0

print("ok boss")
while(True):
    ascentState = GPIO.input(ascentPin)
    descentState = GPIO.input(descentPin)

    if(mode == 0):
        if(ascentState != lastAscentState):
            if(ascentState == False):        
                goingUp()

                
    elif(mode == 1):# playing and waiting for pause
        if(time.time() > timeToPause):
            if(height == 0):
                print("going idle")
                mode = 0
                os.system('killall omxplayer.bin')
                omxc = Popen(['omxplayer', '-b', '--loop', slideshow], stdin=PIPE, stdout=PIPE, close_fds=True)

            else:
                omxc.stdin.write("p")
                #os.system('killall omxplayer.bin')
                timeToHang = time.time() + 10
                mode = 2
            
    elif(mode == 2): #hanging and waiting for input or timeout
        if(ascentState != lastAscentState):
            if(ascentState == False):        
                goingUp()
                    
        elif(descentState != lastDescentState):
            if(descentState == False):
                goingDown()
                

        elif(time.time() > timeToHang):
            os.system('killall omxplayer.bin')
            omxc = Popen(['omxplayer', '-b', '--loop', slideshow], stdin=PIPE, stdout=PIPE, close_fds=True)
            mode = 0
            height = 0

    lastAscentState=ascentState
    lastDescentState = descentState

