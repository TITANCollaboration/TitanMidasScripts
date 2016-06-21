#!/home/mpet/local/bin/python2.7

from midas2eva import SDA
from collections import Counter
import json
import extractFromPerlRCLog as exprc


def getjson(filename):
    '''Extract the TOF data from the given filename and create
    a JSON data structure from it.

    f: The position in the frequency list
    c: The tof channel of a count
    N: Number of ions counted in channel 'c'
    countclass: the total number of ions in the event
    invcc: 1/countclass -> A hack to get the count class histogram
           to appear correctly in prcview.html
    '''
    M2E = SDA(filename)
    M2E.versionMID = 2
    M2E.extractXML()
    M2E.getStartFreq(None)
    M2E.getStopFreq(None)
    M2E.getStartTime(None)
    M2E.getEndTime(None)
    M2E.getNumFreqSteps(None)
    M2E.getNumCycles()
    M2E.getCycleTime()
    M2E.getElem(None)
    M2E.getZ(None)
    M2E.collectMdumpData()
    M2E.reorganizeMdumpData()
    M2E.binMdumpData(0.2, 200)

    bindata = M2E.getbindata()

    numFreq = M2E.numfreqsteps
    jsonData = []
    for i in xrange(len(bindata)):
        hist = Counter(bindata[i])
        countclass = sum(hist.values())
        if countclass == 0:
            invcc = 0
        else:
            invcc = 1. / float(countclass)
        for j in hist:
            jsonData.append({'f': i % numFreq, 'c': j, 'N': hist[j],
                             'countclass': countclass,
                             'invcc': invcc})

    return jsonData


def getAllJson():
    '''
    Gather the JSON data from all of the files in the PerlRC.log
    file for the last scan.
    '''
    prc = exprc.extractFromPerlRCLog()

    prc.get_last_scan()
    prc.last_scan_runs()
    prc.last_scan_filenames()
    files = prc.runFilenames

    date = prc.last_scan_date()

    # Get the files with path
    files = [prc.datapath + date + '/' + f for f in files]

    # Get the JSON data
    data = [getjson(f) for f in files]

    scanvals = prc.last_scan_values()
    scanvar = prc.last_scan_variable()

    # Added the scan variable and scan values into the
    # JSON data.
    for d, y in zip(data, scanvals):
        for x in d:
            x['scanval'] = float(y)
            x['scanvar'] = scanvar
            x['scan'] = 1

    # If the scan is 2D, change the 'scan' to 2, to allow for the
    # second plot in prcview.html
    if prc.last_scan_type() == "Scan2D":
        for d in data[1::2]:
            for x in d:
                x['scan'] = 2

    # flatten the JSON data.
    # Also include the last scan text from the log file,
    # to display on the prcview.html
    return [flatten(data), prc.lastScan]


def dumpJson():
    '''
    Write the JSON data to jsondump.json

    This file is included in the MIDAS ODB, so that it can be accessed with the
    MIDAS web server.
    '''
    data, rawLastScan = getAllJson()
    with open('/home/mpet/online/custom/jsondump.json', 'w') as outfile:
        #json.dump(data, outfile, indent=4, separators=(',', ': '))
        json.dump([rawLastScan, data], outfile, indent=4,
                  separators=(',', ': '))


def flatten(a, result=[]):
    '''
    Convience function to flatten lists.
    '''
    for elem in a:
        if isinstance(elem, list):
            flatten(elem, result)
        else:
            result.append(elem)

    return result

if __name__ == "__main__":
    dumpJson()
