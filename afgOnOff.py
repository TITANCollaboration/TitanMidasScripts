#!/home/mpet/local/bin/python2.7
#import sys
#sys.path.append('/home/mpet/Aaron/TitanMidasScripts/pythonmidas')

#from afgcontrol import afg
#import pythonmidas.pythonmidas as Midas
import afg

mpetafg = afg.quad_afg()
mpetafg.openConnection()
mpetafg.afgOnOffOffOn()
mpetafg.closeConnection()

