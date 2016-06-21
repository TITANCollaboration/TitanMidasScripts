#!/home/mpet/local/bin/python2.7

import extractFromPerlRCLog as prc
import perlRCjsonData as jd

x = prc.extractFromPerlRCLog()

x.convert_PerlRC()

jd.dumpJson()
