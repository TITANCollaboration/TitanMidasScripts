#!/bin/bash
#

# Kill any old copies of python that might still be running
killall python2.7_copy

# Program the quadrupole afg
/home/mpet/local/bin/python2.7_copy /home/mpet/local/scripts/afgSetFreqList.py

# Program the dipole afg
/home/mpet/local/bin/python2.7_copy /home/mpet/local/scripts/afgSetDipoleFreqList.py
