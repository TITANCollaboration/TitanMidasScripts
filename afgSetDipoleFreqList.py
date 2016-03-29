#!/home/mpet/local/bin/python2.7

import afg

try:
    myafg = afg.swift_afg()
    myafg.afgSetTigger()
    myafg.afgSetOutputLoad()
    myafg.afgSetFreqList()
    myafg.closeConnection()
except:
    pass

# If an afg is to be in burst mode, program it here
try:
    burst = afg.burst_afg()
    burst.afgSetTigger()
    burst.afgSetOutputLoad()
    burst.afgSetFreqList()
    burst.closeConnection()
except:
    pass
