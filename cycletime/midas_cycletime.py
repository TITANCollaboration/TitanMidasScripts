#import sys
#sys.path.append("/home/mpet/Aaron/TitanMidasScripts/pythonmidas/")

import cycletime as ct
import pythonmidas.pythonmidas as Midas

try:
    runtime = ct.run_time()
    msg = "The next run will take: " + str(runtime) + " min."
except Exception as e:
    #msg = "There was an error running tri_config. " +\
    #    "Please check ppg settings and/or hardware"
    msg = "Error: " + str(e)

Midas.sendmessage("CycleTime", msg)
