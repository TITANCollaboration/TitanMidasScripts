#!/usr/bin/python
# A.A. Kwiatkowski October 2014
# stop TIS FIL, based off stopRFQ.py

import pythonmidas.pythonmidas as Midas

Midas.sendmessage("Alarm:", "TIS:IG1 pressure too high: Kill TIS1 FIL")

print Midas.varget("/Equipment/Beamline/Variables/Measured[129]")

# The Demand isn't set again if it is the same value as previously used.
print Midas.varset("/Equipment/Beamline/Variables/Demand[129]", 1)
print Midas.varset("/Equipment/Beamline/Variables/Demand[129]", 0)
