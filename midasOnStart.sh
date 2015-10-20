#!/bin/bash
#

# Kill any old copies of python that might still be running
killall python2.7_copy
# Program the quadrupole afg
/home/mpet/local/bin/python2.7_copy /home/mpet/local/scripts/afgSetFreqList.py
# Program the dipole afg
/home/mpet/local/bin/python2.7_copy /home/mpet/local/scripts/afgSetDipoleFreqList.py


################################

#sleep 1

#perl /home/mpet/Aaron/TitanMidasScripts/swiftStartMenuOnOff.pl
#echo $?
#AFGOnOff=`echo $?`

#perl /home/mpet/Aaron/TitanMidasScripts/setFreqList.pl
#echo $?
#AFGFreqSet=`echo $?`

#perl /home/mpet/Aaron/TitanMidasScripts/setFreqList.pl
#perl /home/mpet/Aaron/TitanMidasScripts/setFreqList.pl

#perl /home/mpet/Aaron/TitanMidasScripts/getRFAmp.pl
#/home/mpet/Aaron/TitanMidasScripts/autoroody.sh

# Return the error states of the above scripts.
# Exit with 0, everything passed,
# any other value indicates an error.
#echo $AFGOnOff, $AFGFreqSet
#exit $(($AFGOnOff + $AFGFreqSet))
