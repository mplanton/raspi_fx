#!/usr/bin/env python3

import RPi.GPIO as GPIO
from RPLCD import CharLCD
from time import sleep

# init
lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=4, pin_e=17, pins_data=[18, 22, 23, 24])

# write string
lcd.write_string('Hello world!')

# write string to second line on 4th column
lcd.cursor_pos = (1, 3)
lcd.write_string('Huhu')

sleep(2)
lcd.clear()
sleep(1)

while True:
  lcd.write_string("This will loop")
  lcd.cursor_pos=(1, 4)
  lcd.write_string("forever...")
  sleep(1)
  lcd.clear()
  sleep(1)
