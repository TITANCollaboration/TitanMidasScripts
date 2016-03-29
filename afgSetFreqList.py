#!/home/mpet/local/bin/python2.7
import afg
import pythonmidas.pythonmidas as midas
import time

try:
    #mpetafg = afgcontrol.afg()
    mpetafg = afg.quad_afg()
    mpetafg.openConnection()
    mpetafg.afgSetOutputLoad()
    mpetafg.afgSetTigger()
    mpetafg.afgStartMenuOnOff()
    mpetafg.afgSetFreqList()
    mpetafg.closeConnection()
except:
    print "Failure."
    # Sleep 10s so that run starts, and then we can stop it.
    time.sleep(10)
    midas.stoprun()
    midas.sendmessage('AFGCONTROLERROR',
                      'Quadrupole AFG not programmed correctly. Abort.')
