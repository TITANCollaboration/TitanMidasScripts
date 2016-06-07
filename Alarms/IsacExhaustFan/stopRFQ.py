#!/usr/bin/python
# A.A. Kwiatkowski February 2013
# stop RFQ PSD, based off A.T. Gallant's test.py

import pythonmidas.pythonmidas as Midas

#print "\nTesting sendmessage: name=test msg=test message"
Midas.sendmessage("Alarm:", "An ISAC Exhaust Fan has failed: Kill RFQ PSD")

print Midas.varget("/Equipment/Beamline/Variables/Measured[124]")

# The Demand isn't set again if it is the same value as previously used.
Midas.varset("/Equipment/Beamline/Variables/Demand[124]", 1)
Midas.varset("/Equipment/Beamline/Variables/Demand[124]", 0)
