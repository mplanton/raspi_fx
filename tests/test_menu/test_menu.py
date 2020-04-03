#!/usr/bin/env python3

class Node:
  """Tree Node"""
  def __init__(self, name, data=None, parent=None, children=None):
    self.name = name
    self.data = data
    self.parent = parent
    self.children = children

  def __str__(self):
    # return a string from the root down to this node
    if self.parent == None:
      # root
      return "/" + self.name
    else:
      return str(self.parent) + "/" + self.name

  def render_tree(self, level=0):
  # return a string which represents the tree starting at this node
    ret = "  "*level + "*" + self.name + "\n"
    
    if type(self.children) == type(None):
      # leaf
      pass
    elif type(self.children) == list:
      for child in self.children:
        ret += child.render_tree(level+1)
    else:
      ret += self.children.render_tree(level+1)
    return ret


if __name__ == "__main__":
  metering = Node("metering")
  
  choose_fx = Node("choose effect")
  
  choose_params = Node("choose parameters")
  presets = Node("presets")
  
  adj_params = Node("adjust parameters")


  
  metering.children = choose_fx
  
  choose_fx.parent = metering
  choose_fx.children = [choose_params, presets]

  choose_params.parent = choose_fx
  choose_params.children = adj_params
  
  presets.parent = choose_fx
  
  adj_params.parent = choose_params
  
  
  print(choose_params)
  print(presets)
  print(metering)
  
  print()
  
  print("full tree:")
  print(metering.render_tree())
  print()
  print("a part of it:")
  print(choose_fx.render_tree())
