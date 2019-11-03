from time import sleep
import RPi.GPIO as GPIO
from pyOSC3 import OSC3
from RPLCD import CharLCD
import KY040
import Button

class Effect:
  """class to represent effects in the menu"""
  def __init__(self, name, params):
    """Constructor
    Args:
        name: name of the effect
        params: a dictionary of parameter value pairs of the effect

    Constants:
        MIN_VAL: minimum value of parameter range
        MAX_VAL: maximum value of parameter range
    """
    self.MIN_VAL = 0
    self.MAX_VAL = 127
    self.name = name
    self.params = params
    # TODO: implement presets -> store and load params from disk


class Menu:
  """Menu class for managing a multi effects patch in Pd on Raspberry Pi.

  The Menu is operated via a rotary encoder with an integrated push button.
  Another button is added to navigate the Menu.
  Turning the rotary encoder selects menu options or changes effects parameters.
  Pushing the encoders internal push button increases the menu level and pushing
  the other button decreases the menu level.

  The menu levels are:
   0. Level Metering
   1. Effect Selection
   2. Parameter Selection
   3. Parameter Adjustment

  The Menu is displayed on a HD44780 compatible 2x16 character display.

  Pd and the Menu communicate via OSC messages and listen on different ports.

  This menu is designed to display true effects parameters values, even if these
  values are changed by a different source like a MIDI controller.

  Manuel Planton 2019
  """

  OSC_ADDRESS = "/menu"
  LEVEL_MIN = 0
  LEVEL_MAX = 3
  SUPERLINE = "#"*16

  def __init__(self, ip, port, pd_ip, pd_port, d_rs, d_rw, d_e, d_d4, d_d5, d_d6, d_d7, r_clk, r_d, r_sw, button):
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
        d_rw: HD44780 read/write pin number
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

    self.ip = ip
    self.port = port
    self.pd_ip = pd_ip
    self.pd_port = pd_port
    self.pd_is_connected = False

    self.rotary_increment = 1

    # menu level entry state
    self.level = 1
    # current effect
    self.fx_nr = 0
    # current parameter of the effect
    self.param_nr = 0

    # define effects
    main = Effect(name = "main", params = {'on' : 1, 'in_vol' : 127, 'out_vol' : 127})
    reverb = Effect(name = "reverb", params = {'on' : 0, 'dry' : 64, 'wet' : 120, 'rev_in_lvl' : 100,
                                               'liveness' : 80, 'fc' : 40, 'hf_damp' : 7})
    delay = Effect("delay", {'on' : 0, 'dry' : 64, 'wet' : 127, 'delay_time' : 64, 'feedback' : 100,
                             'fc_lop' : 120, 'fc_hip' : 25, 'detune' : 10, 'mod_freq' : 5})
    lop = Effect("lop", {'on' : 0, 'fc' : 64})
    hip = Effect("hip", {'on' : 0, 'fc' : 30})
    # effects list
    self.fx = [main, reverb, delay, lop, hip]

    GPIO.setmode(GPIO.BCM)
    self.button = Button.Button(button, "falling", self.buttonPressed)

    # callbacks for encoder and OSC handlers must be defined
    self.r_encoder = KY040.KY040(r_clk, r_d, r_sw, self.rotaryChange, self.switchPressed)
    print("DBG: initialize display")
    # Compat mode is true because slow displays show garbage sometimes.
    self.lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=d_rs, pin_rw=d_rw, pin_e=d_e,
                       pins_data=[d_d4, d_d5, d_d6, d_d7], compat_mode = True)
    print("DBG: initialize OSC Server")
    self.server = OSC3.OSCServer((ip, port))
    print("DBG: initialize OSC Client")
    self.client = OSC3.OSCClient()

    # first appearance of the menu
    self.printMenu()


  def buttonPressed(self, pin):
    """Callback function for the single push button"""
    print("DBG: button pressed")
    if self.level > self.LEVEL_MIN:
      self.level = self.level - 1
      self.printMenu()


  def switchPressed(self, pin):
    """Callback function for pressing the internal button of the rotary encoder
    Args:
        pin: BCM pin number of the button
    """
    print("DBG: rotary button pressed")
    # try to connect to Pd if it has not been done successfully
    if(self.pd_is_connected == False):
      self.connectToPd()
    if self.level < self.LEVEL_MAX:
      self.level = self.level + 1
      # update all parameters of the effect
      self.updateParameters()
      self.printMenu()
    elif self.level == self.LEVEL_MAX:
      # change rotary encoder increment if switch pressed on parameter adjustment level
      if self.rotary_increment == 1:
        self.rotary_increment = 5
      elif self.rotary_increment == 5:
        self.rotary_increment = 10
      elif self.rotary_increment == 10:
        self.rotary_increment = 25
      elif self.rotary_increment == 25:
        self.rotary_increment = 1


  def rotaryChange(self, direction):
    """Callback function for turning the rotary encoder
    Args:
        direction: 1 - clockwise, -1 - counterclockwise
    """
    print("DBG: turned: ", str(direction))

    # level 0 is metering -> do nothing
    if self.level <= 0:
      return

    if self.level == 1:
      # effect selection
      new_fx_nr = self.fx_nr + direction
      if new_fx_nr in range(0, len(self.fx)):
        self.fx_nr = new_fx_nr
        self.param_nr = 0
        self.printMenu()

    elif self.level == 2:
      # parameter selection
      new_param_nr = self.param_nr + direction
      if new_param_nr in range(0, len(self.fx[self.fx_nr].params)):
        self.param_nr = new_param_nr
        self.printMenu()

    elif self.level == 3:
      # parameter adjustment
      current_fx = self.fx[self.fx_nr]
      keys = list(current_fx.params.keys())
      key = keys[self.param_nr]
      new_val = current_fx.params[key] + (direction * self.rotary_increment)

      if new_val < current_fx.MIN_VAL:
        new_val = current_fx.MIN_VAL
      elif new_val > current_fx.MAX_VAL:
        new_val = current_fx.MAX_VAL

      # on is handled differently
      if key == 'on':
        current_fx.params[key] = int(not current_fx.params[key])
      else:
        current_fx.params[key] = new_val

      self.setParameter()
      self.printMenu()

    else:
      print("ERROR: no such level!")


  def printMenu(self):
    print("DBG:", "lvl:", str(self.level))
    print("DBG:", "fx_nr:", str(self.fx_nr))
    print("DBG:", "param_nr:", str(self.param_nr))

    # metering
    if self.level == 0:
      self.lcd.clear()
      self.lcd.cursor_pos = (0,0)
      self.lcd.write_string("Menu lvl 0")
      self.lcd.cursor_pos = (1,0)
      self.lcd.write_string("Metering: TBA")

    # effect selection
    elif self.level == 1:
      self.lcd.clear()
      if self.fx_nr == len(self.fx) - 1: # last entry
        on = self.fx[self.fx_nr].params['on']
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string("*" + self.fx[self.fx_nr].name + " " + str(on))
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string(self.SUPERLINE)
      else:
        self.lcd.cursor_pos = (0,0)
        on_1 = self.fx[self.fx_nr].params['on']
        self.lcd.write_string("*" + self.fx[self.fx_nr].name + " " + str(on_1))
        self.lcd.cursor_pos = (1,0)
        on_2 = self.fx[self.fx_nr + 1].params['on']
        self.lcd.write_string(" " + self.fx[self.fx_nr + 1].name + " " + str(on_2))

    # parameter selection and adjustment
    elif self.level == 2 or self.level == 3:
      params = self.fx[self.fx_nr].params
      keys = list(params.keys())
      key1 = keys[self.param_nr]

      if self.level == 2:
        crsr = "*"
      else:
        crsr = ">"

      self.lcd.clear()

      # last entry
      if self.param_nr == len(params) - 1:
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string(crsr + key1 + ": " + str(params[key1]))
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string(self.SUPERLINE)
      else:
        key2 = keys[self.param_nr + 1]
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string(crsr + key1 + ": " + str(params[key1]))
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string(" " + key2 + ": " + str(params[key2]))

    else:
      print("ERROR: no such menu level")


  def setParameter(self):
    msg = OSC3.OSCMessage()
    keys = list(self.fx[self.fx_nr].params.keys()) # TODO: this should be more efficient and convenient
    key = keys[self.param_nr]
    msg.setAddress("/pd/" + self.fx[self.fx_nr].name + "/set/" + key)
    msg.append(self.fx[self.fx_nr].params[key])
    self.client.send(msg)


  def getParameter(self, key):
    msg = OSC3.OSCMessage()
    msg.setAddress("/pd/" + self.fx[self.fx_nr].name + "/get/" + key)
    msg.append("bang")
    self.client.send(msg)


  def updateParameters(self):
    params = self.fx[self.fx_nr].params
    for key in self.fx[self.fx_nr].params:
      self.getParameter(key)


  def connectToPd(self):
    # it is possible to tell Pd the ip and the port to connect to
    print("DBG: Try to let Pd connect to menu's server")
    self.oscSend("/pd/connect", "bang")


  def handleGetParameter(self, addr, tags, data, client_address):
    # Messages to menu should be exclusively from Pd or to what it should be connected
    if self.pd_is_connected == False:
      self.pd_is_connected = True
    # safer, but more expensive -> search name of effect according to data
    key = data[-2]
    value = data[-1]
    self.fx[self.fx_nr].params[key] = int(value)


  def oscSend(self, address, data):
    msg = OSC3.OSCMessage()
    msg.setAddress(address)
    msg.append(data)
    self.client.send(msg)


  def run(self):
    self.r_encoder.start()
    self.button.start()
    print("connect menu OSC client to", self.pd_ip, "at port", str(self.pd_port))
    self.client.connect((self.pd_ip, self.pd_port))
    self.server.addMsgHandler('/menu', self.handleGetParameter)
    print("running...")
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
  # use BCM pin numbers
  D_RS = 4
  D_RW = 25
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

  m = Menu(IP, PORT, IP, PD_PORT, D_RS, D_RW, D_E, D_D4, D_D5, D_D6, D_D7, R_CLK, R_D, R_SW, B_PIN)
  m.run() # runs forever...
  m.stop()
  print("program terminated")
