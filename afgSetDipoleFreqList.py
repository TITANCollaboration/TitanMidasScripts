#!/home/mpet/local/bin/python2.7

#import sys
#sys.path.append('/home/mpet/Aaron/TitanMidasScripts/pythonmidas')

#import swift_dipole_freqlist as sdf
import afg

#afg = sdf.SwiftDipole()
myafg = afg.swift_afg()

myafg.afgSetOutputLoad()
myafg.afgSetTigger()
myafg.afgSetFreqList()
myafg.closeConnection()
