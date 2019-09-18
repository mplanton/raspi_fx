#!/usr/bin/env python3
"""
A script to convert values from a rotary encoder to OSC messages.
Manuel Planton 2019
"""

from pyOSC3 import OSC3 as OSC
import RPi.GPIO as GPIO
from time import sleep
from classes import KY040


if __name__ == "__main__":
    CLOCKPIN = 26
    DATAPIN = 20
    SWITCHPIN = 21

    # connect client to OSC server
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 7110))
    # different ip for PC
    #c.connect(('169.254.178.186', 7110))

    # OSC messages
    switch_msg = OSC.OSCMessage()
    switch_msg.setAddress("/rotary/switch")
    switch_msg.append("1")

    rotary_msg = OSC.OSCMessage()
    rotary_msg.setAddress("/rotary/encoder")

    # define callbacks
    def rotaryChange(direction):
        print("turned - ", str(direction))
        rotary_msg.clearData()
        if direction == 0:
            # clockwise
            rotary_msg.append(0)
        else:
            # anticlockwise
            rotary_msg.append(1)
        c.send(rotary_msg)

    def switchPressed(pin):
        print("button connected to pin:{} pressed".format(pin))
        c.send(switch_msg)

    # start encoder
    GPIO.setmode(GPIO.BCM)
    r_encoder = KY040.KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChange, switchPressed)
    print('Start Encoder')
    r_encoder.start()


    print('Start program loop...')
    try:
        while True:
            sleep(10)
            print('Ten seconds...')
    finally:
        print('Stopping GPIO monitoring...')
        r_encoder.stop()
        GPIO.cleanup()
        print('Program ended.')

