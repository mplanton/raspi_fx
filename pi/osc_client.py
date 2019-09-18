#!/usr/bin/env python3

# osc client

from pyOSC3 import OSC3 as OSC

c = OSC.OSCClient()
c.connect(('127.0.0.1', 7110))

oscmsg = OSC.OSCMessage()
oscmsg.setAddress("/startup")
oscmsg.append('HELLO')
c.send(oscmsg)
