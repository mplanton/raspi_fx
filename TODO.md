TODO:
=====

- bypass der effekte implementieren

- Reihenfolge der Effekte bestimmen (was seriell/parallel?)

- Parameter der Effekte vom Menü aus vom Pd Patch aktualisieren (zeigt in manchen Situationen falsche Werte an, wenn noch nichts verstellt wurde. Z.B. wenn das Menü nachträglich neu gestartet wird und der Pd Patch durch läuft)

- Effekt Klasse in eigene Datei. Aus Menu Klasse entfernen

- Presets für Effekte implementieren
  * neuen Branch für dieses Feature
  * Neue Struktur des Menüs erstellen -> Verzweigungen möglich
    - bis jetzt gibt es nur linear Level
    - Jede Menü Ebene ist ein Objekt/Klasse
    - Baumstruktur von Objekten
  * Effektparameter speichern/laden -> main ist individuell eingestellt

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

-> Lösung in LCD Klasse -> compat_mode = True
