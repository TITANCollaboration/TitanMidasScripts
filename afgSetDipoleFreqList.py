#!/home/mpet/local/bin/python2.7

#import sys
#sys.path.append('/home/mpet/Aaron/TitanMidasScripts/pythonmidas')

#import swift_dipole_freqlist as sdf
import afg

#afg = sdf.SwiftDipole()
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
