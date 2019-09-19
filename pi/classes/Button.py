import RPi.GPIO as GPIO
from time import sleep

class Button:
  DEBOUNCE_TIME = 200 # change this if needed

  def __init__(self, button_pin, edge, pressedCallback):
    """Constructor
    Args:
        button_pin: pin number the button is connected to
        edge: start callback function on rising, falling or both slopes
              strings "rising", "falling" or "both"
        pressedCallback: A callback function to be executed, when the button is pressed
    """
    self.pin = button_pin

    if edge == "rising":
      self.edge = GPIO.RISING
    elif edge == "falling":
      self.edge = GPIO.FALLING
    elif edge == "both":
      self.edge = GPIO.BOTH
    else:
      print("Button: wrong param for edge!")

    self.callback = pressedCallback
    GPIO.setup(button_pin, GPIO.IN) # get your own resistor of 10k to 100k

  def start(self):
    GPIO.add_event_detect(self.pin, self.edge, self._callback, self.DEBOUNCE_TIME)

  def stop(self):
    GPIO.remove_event_detect(self.pin)

  def _callback(self, pin):
    self.callback(pin)


if __name__ == "__main__":
  PIN = 5
  GPIO.setmode(GPIO.BCM)
  def buttonPressed(pin):
    print("button pressed at pin " + str(pin))

  button = Button(PIN, "falling", buttonPressed)
  button.start()
  print("press button...")

  sleep(20)

  button.stop()
  GPIO.cleanup()
  print("program terminated")
