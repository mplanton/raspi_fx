TODO:
=====

- on/off für effekte implementieren mit [switch~] um cpu zu sparen

- Presets für Effekte implementieren

- Menü Level 0: Metering implementieren

- statt self.param_nr und nur dict von params evtl. key speichern
  -> das geht effizienter und einfacher
  
- eventuell latenz verbessern für nicht send effekte

- Effekte implementieren
  * Flanger
  * Physical Modeling Plate Reverb
  * Phaser
  * Chorus (random LFO -> wie klingt das?) (EHX Stereo Poly Chorus)
  * Envelope Follower
    * auto filter (Bandpass/Peak, Bandsperre)
  * Distortion (Upsampling!) (alle möglichen Kennlinien)
  * Faltungshall
  * Physical Modeling Spring Reverb
  * Resonator Bank
  * Autotune
  * Kompressor/Limiter
  * Polyphoner Pitch Shifter
  * Stereo Delay
  * Granular Delay/Hall/sonstige Effekte

- Debug messages entfernen (weniger augaben -> bessere performance)

- Bug: Display zeigt selten Müll an, wenn rotary encoder gedreht wird
DBG: param_nr: 0
DBG: turned:  1
DBG: lvl: 1
DBG: fx_nr: 3
DBG: param_nr: 0
DBG: turned:  1
DBG: lvl: 1
DBG: fx_nr: 4
DBG: param_nr: 0
DBG: turned:  1
DBG: turned:  1
DBG: turned:  -1
DBG: lvl: 1
DBG: fx_nr: 3
DBG: param_nr: 0
DBG: turned:  1
DBG: lvl: 1
DBG: fx_nr: 4
DBG: param_nr: 0
DBG: turned:  1
Traceback (most recent call last):
  File "/home/pi/classes/KY040.py", line 45, in _clockCallback
    self.rotaryCallback(self.ANTICLOCKWISE)
  File "/home/pi/classes/Menu.py", line 176, in rotaryChange
DBG: turned:  1
    self.printMenu()
  File "/home/pi/classes/Menu.py", line 230, in printMenu
    self.lcd.write_string(" " + self.fx[self.fx_nr + 1].name)
IndexError: list index out of range

