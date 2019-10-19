TODO:
=====

- on/off für effekte implementieren mit [switch~] um cpu zu sparen

- überflüssige in und out gains von delay und reverb entfernen

- Presets für Effekte implementieren

- Taster besser entprellen (zählt oft 2 mal) -> hw?

- Rotary Encoder zu langsam und zu ungenau 
  -> HW-Debounce mit Kondensator? Und auch für Taster?

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

- Bug: Manchmal wird nach einer Zeit nur mehr Blödsinn am LCD angezeigt.
