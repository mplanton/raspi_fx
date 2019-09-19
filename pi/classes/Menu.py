from time import sleep
import RPi.GPIO as GPIO
from pyOSC3 import OSC3
import hd44780
import KY040
import Button

class Menu:
  """Menu class for managing a multi effects patch in Pd on Raspberry Pi.

  The Menu is operated via a rotary encoder with an integrated push button.
  Another button is added to navigate the Menu.
  Turning the rotary encoder selects menu options or changes effects parameters.
  Pushing the encoders internal push button increases the menu level and pushing
  the other button decreases the menu level.

  The menu levels are:
   1. Level Metering
   2. Effect Selection
   3. Parameter Selection
   4. Parameter Adjustment

  The Menu is displayed on a HD44780 compatible 2x16 character display.

  Pd and the Menu communicate via OSC messages and listen on different ports.

  This menu is designed to display true effects parameters values, even if these
  values are changed by a different source like a MIDI controller.

  Manuel Planton 2019
  """

  def __init__(self, ip, port, pd_ip, pd_port, d_rs, d_e, d_d4, d_d5, d_d6, d_d7, r_clk, r_d, r_sw, button):
    """Constructor
    IP addresses and port numbers for OSC connection are needed.
    Prefix 'd' is for HD44780 compatible display connections connected to the pins of the RPi.
    Prefix 'r' is for KY040 compatible rotary encoder connections connected to the pins of the RPi.
    Pin numbers are BCM numbers! (see GPIO.setmode(GPIO.BCM))

    Args:
        ip: IP Address of the OSC server of this menu
        port: port number of the OSC server of this menu
        pd_ip: IP Address of  the OSC server of the Pd effects patch
        pd_port: port number of the OSC server of the Pd effects patch
        d_rs: HD44780 register select pin number
        d_e: HD44780 enable pin number
        d_d4: HD44780 data channel 4 pin number
        d_d5: HD44780 data channel 5 pin number
        d_d6: HD44780 data channel 6 pin number
        d_d7: HD44780 data channel 7 pin number
        r_clk: rotary encoder clock pin number
        r_d: rotary encoder data pin number
        r_sw: rotary encoder internal switch button pin number
        button: push button pin number
    """

    GPIO.setmode(GPIO.BCM)

    self.button = Button.Button(button, "falling", self.buttonPressed)
    # callbacks for encoder must be defined first
    self.r_encoder = KY040.KY040(r_clk, r_d, r_sw, self.rotaryChange, self.switchPressed)
    print("initialize display")
    self.display = hd44780.HD44780(d_rs, d_e, d_d4, d_d5, d_d6, d_d7)
    print("initialize OSC Server")
    self.server = OSC3.OSCServer((ip, port))
    print("initialize OSC Client")
    self.client = OSC3.OSCClient()
    self.client.connect((pd_ip, pd_port))

  def buttonPressed(self, pin):
    """Callback function for the single push button"""
    print("button pressed at pin " + str(pin))

  def rotaryChange(self, direction):
    """Callback function for turning the rotary encoder
    Args:
        direction: 0 - clockwise, 1 - counterclockwise
    """
    print("turned: ", str(direction))

  def switchPressed(self, pin):
    """Callback function for pressing the internal button of the rotary encoder
    Args:
        pin: BCM pin number of the button
    """
    print("rotary button pressed")



  def run(self):
    print("running...")
    self.r_encoder.start()
    self.button.start()
    self.server.serve_forever()

  def stop(self):
    self.r_encoder.stop()
    self.button.stop()
    GPIO.cleanup()

if __name__ == "__main__":
  # OSC
  IP = '127.0.0.1' # localhost
  PORT = 7111
  PD_PORT = 7110
  # display
  D_RS = 4
  D_E = 17
  D_D4 = 18
  D_D5 = 22
  D_D6 = 23
  D_D7 = 24
  # rotary encoder
  R_CLK = 26
  R_D = 20
  R_SW = 21
  # push button
  B_PIN = 5

  m = Menu(IP, PORT, IP, PD_PORT, D_RS, D_E, D_D4, D_D5, D_D6, D_D7, R_CLK, R_D, R_SW, B_PIN)
  m.run()
  print("running...")
  sleep(20)
  m.stop()
  print("program terminated")
