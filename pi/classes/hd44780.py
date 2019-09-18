#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

"""
HD44780 compatible display driver for 4 bit mode
RW select is set to write for convenience (use it for more professional projects)
Manuel Planton 2019
"""

class HD44780:
    WIDTH = 16          # characters per line
    LINE_1 = 0x80       # set DDRAM address to beginning of line 1
    LINE_2 = 0xC0       # set DDRAM address to beginning of line 2
    CHR = GPIO.HIGH     # register select on = R/W DDRAM or CGRAM
    CMD = GPIO.LOW      # all other commands
    E_PULSE = 0.0005
    E_DELAY = 0.0005

    def __init__(self, rs, e, d4, d5, d6, d7):
        # set GPIO Pins
        self.rs = rs # regsiter select
        self.e  = e # enable
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7 = d7
        # initialisation
        self.pins_init()
        self.display_init()

    def send_byte(self, bits, mode):
        # send high nibble

        # set pins to low
        GPIO.output(self.rs, mode)
        GPIO.output(self.d4, GPIO.LOW)
        GPIO.output(self.d5, GPIO.LOW)
        GPIO.output(self.d6, GPIO.LOW)
        GPIO.output(self.d7, GPIO.LOW)

        # set ones
        if bits & 0x10 == 0x10:
            GPIO.output(self.d4, GPIO.HIGH)
        if bits & 0x20 == 0x20:
            GPIO.output(self.d5, GPIO.HIGH)
        if bits & 0x40 == 0x40:
            GPIO.output(self.d6, GPIO.HIGH)
        if bits & 0x80 == 0x80:
            GPIO.output(self.d7, GPIO.HIGH)
        time.sleep(self.E_DELAY)
        GPIO.output(self.e, GPIO.HIGH)
        time.sleep(self.E_PULSE)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(self.E_DELAY)


        # send low nibble

        GPIO.output(self.d4, GPIO.LOW)
        GPIO.output(self.d5, GPIO.LOW)
        GPIO.output(self.d6, GPIO.LOW)
        GPIO.output(self.d7, GPIO.LOW)

        # set ones
        if bits&0x01==0x01:
            GPIO.output(self.d4, GPIO.HIGH)
        if bits&0x02==0x02:
            GPIO.output(self.d5, GPIO.HIGH)
        if bits&0x04==0x04:
            GPIO.output(self.d6, GPIO.HIGH)
        if bits&0x08==0x08:
            GPIO.output(self.d7, GPIO.HIGH)
        time.sleep(self.E_DELAY)
        GPIO.output(self.e, GPIO.HIGH)
        time.sleep(self.E_PULSE)
        GPIO.output(self.e, GPIO.LOW)
        time.sleep(self.E_DELAY)

    def display_init(self):
        self.send_byte(0x33, self.CMD) # function set
        self.send_byte(0x32, self.CMD) # function set
        self.send_byte(0x28, self.CMD) # function set to 4 bit mode
        self.send_byte(0x0C, self.CMD) # display on
        self.send_byte(0x06, self.CMD) # entry mode set
        self.send_byte(0x01, self.CMD) # clear display

    def message(self, line, message):
        message = message.ljust(self.WIDTH," ")
        self.send_byte(line, self.CMD)
        for i in range(self.WIDTH):
            self.send_byte(ord(message[i]),self.CHR)


    def pins_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.e, GPIO.OUT)
        GPIO.setup(self.rs, GPIO.OUT)
        GPIO.setup(self.d4, GPIO.OUT)
        GPIO.setup(self.d5, GPIO.OUT)
        GPIO.setup(self.d6, GPIO.OUT)
        GPIO.setup(self.d7, GPIO.OUT)

if __name__ == '__main__':
    disp = HD44780(rs=4, e=17, d4=18, d5=22, d6=23, d7=24)

    disp.message(disp.LINE_1, "Es scheint zu")
    disp.message(disp.LINE_2, "funktionieren :)")

    time.sleep(1)

    msg1 = "Dies ist ein"
    msg2 = "kleiner Test"
    for i in range(len(msg1)):
        disp.message(disp.LINE_1, msg1[:i+1])
        disp.message(disp.LINE_2, "")
        time.sleep(0.05)
    for i in range(len(msg2)):
        disp.message(disp.LINE_1, msg1)
        disp.message(disp.LINE_2, msg2[:i+1])
        time.sleep(0.1)

    time.sleep(4)
    GPIO.cleanup()
