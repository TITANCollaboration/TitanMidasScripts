#!/home/mpet/local/bin/python2.7
#import sys
#sys.path.append('/home/mpet/Aaron/perlRCconvert')
#sys.path.append('/home/mpet/Aaron/perlRCdb')

import extractFromPerlRCLog as prc
import perlRCjsonData as jd

x = prc.extractFromPerlRCLog()
#x.get_last_scan()
#x.last_scan_runs()
#x.output_header()
#x.run_scripts()
x.convert_PerlRC()

jd.dumpJson()
