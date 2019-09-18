#!/bin/bash
# backup data from rspberry pi
# change ip, if needed
rm -drf pi/*
scp -dr pi@169.254.203.219:~/* pi/

