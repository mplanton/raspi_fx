#!/usr/bin/env python3

# usage: osc_server <ip-address> <port>"

import sys
from pyOSC3 import OSC3

def handler(addr, tags, data, client_address):
    txt = "OSCMessage '%s' from %s: " % (addr, client_address)
    txt += str(data)
    print(txt)

if __name__ == "__main__":
    ip = '127.0.0.1' # lacalhost
    port = 7110

    # get optional first arg
    if((len(sys.argv) > 1)):
        if(sys.argv[1] in ('-h', '--help')):
            print("usage:", sys.argv[0], "[-h] <ip-address> <port>")
            print("ip-address default: 127.0.0.1")
            print("port default: 7110")
            exit(0)
        else:
            ip = sys.argv[1] # get ip from first argument

    # get optional second arg port
    if(len(sys.argv) > 2):
        port = int(sys.argv[2])


    # listen on localhost, port 7110
    s = OSC3.OSCServer((ip, port))

    # call handler() for OSC messages received with the '/startup' address
    s.addMsgHandler('/rotary/encoder', handler)
    s.addMsgHandler('/rotary/switch', handler)
    s.addMsgHandler('/rand', handler)
    s.addMsgHandler('/reverb/dry', handler)
    s.addMsgHandler('/reverb/wet', handler)
    s.addMsgHandler('/reverb/rev_in_lvl', handler)
    s.addMsgHandler('/reverb/liveness', handler)
    s.addMsgHandler('/reverb/fc', handler)
    s.addMsgHandler('/reverb/hf_damp', handler)

    print("OSC Server", ip, "at port", port)
    print("OSC Server listening...")
    s.serve_forever()
