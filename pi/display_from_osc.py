#!/usr/bin/env python3

from classes import hd44780
import RPi.GPIO as GPIO
import sys
from pyOSC3 import OSC3

def get_args(argv, ip, port):
    # get optional first arg
    if((len(argv) > 1)):
        if(argv[1] in ('-h', '--help')):
            print("usage:", argv[0], "[-h] <ip-address> <port>")
            print("ip-address default: 127.0.0.1")
            print("port default: 7110")
            exit(0)
        else:
            ip = argv[1] # get ip from first argument

    # get optional second arg port
    if(len(argv) > 2):
        port = int(sys.argv[2])


if __name__ == "__main__":
    ip = '127.0.0.1' # lacalhost
    port = 7110
    get_args(sys.argv, ip, port)

    # display
    d = hd44780.HD44780(rs=4, e=17, d4=18, d5=22, d6=23, d7=24)

    # OSC message handlers
    def encoder_handler(addr, tags, data, client_address):
        txt1 = "%s of %s" % (addr, client_address)
        txt2 = str(data)
        d.message(d.LINE_1, txt1)
        d.message(d.LINE_2, txt2)

    def switch_handler(addr, tags, data, client_address):
        d.message(d.LINE_1, 16*'*')
        d.message(d.LINE_2, 16*'*')

    def rand_handler(addr, tags, data, client_address):
        d.message(d.LINE_1, "rand")
        d.message(d.LINE_2, "value: " + str(data))

    d.message(d.LINE_1, "Starting OSC")
    d.message(d.LINE_2, "ip: " + ip)

    # listen on localhost, port 7110
    s = OSC3.OSCServer((ip, port))

    # call handler() for OSC messages received with the given address
    s.addMsgHandler('/rotary/encoder', encoder_handler)
    s.addMsgHandler('/rotary/switch', switch_handler)
    s.addMsgHandler('/rand', rand_handler)

    print("OSC Server listening...")

    s.serve_forever()
    GPIO.cleanup()
