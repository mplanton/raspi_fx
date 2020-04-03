#!/usr/bin/env python3

import random
import json

class Test:
  def __init__(self, name):
    self.name = name
    self.d = {"cat" : random.randint(1,5), "dog" : random.randint(1,20),
              "horse" : random.randint(1,999)}

  def save_preset(self, preset_name):
    with open(self.name + ".preset", "a") as f:
      preset = "preset " + preset_name + "\n" + \
               json.dumps(self.d, indent=2) + "\n"
      f.write(preset)

  def load_preset(self, preset_name):
    with open(self.name + ".preset", "r") as f:
      # read the whole file and search through it (could be more efficient)
      presets = f.read()
      preset_index = presets.find("preset " + preset_name)
      
      if preset_index >= 0:
        # found it
        print("DBG: preset found at " + str(preset_index))
        
        preset = presets[preset_index:]
        start_index = preset.find('{')
        stop_index = preset.find('}')
        
        print("DBG: string")
        print("DBG: start: " + str(start_index) + " stop: " + str(stop_index))
        print(preset[start_index:stop_index+1])
        
        return json.loads(preset[start_index:stop_index+1])
        
      else:
        # did not find it
        return -1 
        print("DBG: Did not find preset named " + preset_name)

if __name__ == "__main__":
  t1 = Test("object1")
  t2 = Test("object2")
  t3 = Test("another object")
  
#  l = [t1, t2, t3]
#  
#  for obj in l:
#    obj.save_preset("test" + str(random.randint(1, 100)))

  t1_preset = t1.load_preset("test22")
  
  print("got preset:")
  print(t1_preset)
