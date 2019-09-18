#!/usr/bin/python
import time
import RPi.GPIO as GPIO

# HD44780 compatible display driver for 4 bit mode

# RW select is set to write for convenience (use it for more professional projects)

# Zuordnung der GPIO Pins (ggf. anpassen)
LCD_RS = 4 # regsiter select
LCD_E  = 17 # enable
LCD_DATA4 = 18
LCD_DATA5 = 22
LCD_DATA6 = 23
LCD_DATA7 = 24

LCD_WIDTH = 16 		# Zeichen je Zeile
LCD_LINE_1 = 0x80 	# set DDRAM address to beginning of line 1
LCD_LINE_2 = 0xC0 	# set DDRAM address to beginning of line 2
LCD_CHR = GPIO.HIGH	# register select on = R/W DDRAM or CGRAM
LCD_CMD = GPIO.LOW	# all other commands
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_send_byte(bits, mode):
	# send high nibble

	# set pins to low
	GPIO.output(LCD_RS, mode)
	GPIO.output(LCD_DATA4, GPIO.LOW)
	GPIO.output(LCD_DATA5, GPIO.LOW)
	GPIO.output(LCD_DATA6, GPIO.LOW)
	GPIO.output(LCD_DATA7, GPIO.LOW)

	# set ones
	if bits & 0x10 == 0x10:
	  GPIO.output(LCD_DATA4, GPIO.HIGH)
	if bits & 0x20 == 0x20:
	  GPIO.output(LCD_DATA5, GPIO.HIGH)
	if bits & 0x40 == 0x40:
	  GPIO.output(LCD_DATA6, GPIO.HIGH)
	if bits & 0x80 == 0x80:
	  GPIO.output(LCD_DATA7, GPIO.HIGH)
	time.sleep(E_DELAY)
	GPIO.output(LCD_E, GPIO.HIGH)
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, GPIO.LOW)
	time.sleep(E_DELAY)


	# send low nibble

	GPIO.output(LCD_DATA4, GPIO.LOW)
	GPIO.output(LCD_DATA5, GPIO.LOW)
	GPIO.output(LCD_DATA6, GPIO.LOW)
	GPIO.output(LCD_DATA7, GPIO.LOW)

	# set ones
	if bits&0x01==0x01:
	  GPIO.output(LCD_DATA4, GPIO.HIGH)
	if bits&0x02==0x02:
	  GPIO.output(LCD_DATA5, GPIO.HIGH)
	if bits&0x04==0x04:
	  GPIO.output(LCD_DATA6, GPIO.HIGH)
	if bits&0x08==0x08:
	  GPIO.output(LCD_DATA7, GPIO.HIGH)
	time.sleep(E_DELAY)
	GPIO.output(LCD_E, GPIO.HIGH)
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, GPIO.LOW)
	time.sleep(E_DELAY)

def display_init():
	lcd_send_byte(0x33, LCD_CMD) # function set
	lcd_send_byte(0x32, LCD_CMD) # function set
	lcd_send_byte(0x28, LCD_CMD) # function set to 4 bit mode
	lcd_send_byte(0x0C, LCD_CMD) # display on
	lcd_send_byte(0x06, LCD_CMD) # entry mode set
	lcd_send_byte(0x01, LCD_CMD) # clear display

def lcd_message(message):
	message = message.ljust(LCD_WIDTH," ")
	for i in range(LCD_WIDTH):
	  lcd_send_byte(ord(message[i]),LCD_CHR)



def pins_init():
	GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LCD_E, GPIO.OUT)
        GPIO.setup(LCD_RS, GPIO.OUT)
        GPIO.setup(LCD_DATA4, GPIO.OUT)
        GPIO.setup(LCD_DATA5, GPIO.OUT)
        GPIO.setup(LCD_DATA6, GPIO.OUT)
        GPIO.setup(LCD_DATA7, GPIO.OUT)

if __name__ == '__main__':
	pins_init()
	display_init()

	lcd_send_byte(LCD_LINE_1, LCD_CMD)
	lcd_message("Es scheint zu")
	lcd_send_byte(LCD_LINE_2, LCD_CMD)
	lcd_message("funktionieren :)")

	time.sleep(2)

	msg1 = "Dies ist ein bla"
	msg2 = "kleiner Test"
	for i in range(len(msg1)):
		lcd_send_byte(LCD_LINE_1, LCD_CMD)
		lcd_message(msg1[:i+1])
		lcd_send_byte(LCD_LINE_2, LCD_CMD)
		lcd_message("")
		time.sleep(0.1)
	for i in range(len(msg2)):
		lcd_send_byte(LCD_LINE_1, LCD_CMD)
		lcd_message(msg1)
		lcd_send_byte(LCD_LINE_2, LCD_CMD)
		lcd_message(msg2[:i+1])
		time.sleep(0.1)

	time.sleep(4)

	GPIO.cleanup()
