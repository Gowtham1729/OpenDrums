import numpy as np
import serial
import time
from pygame import mixer

PORT_NO = "/dev/ttyACM0"
ard = serial.Serial(PORT_NO, 9600)


mixer.init()
sound = mixer.Sound("samples/909-Clap-1.wav")
sound.play()

while True:
    args = str(ard.readline())
    if args:
        sound.play()
