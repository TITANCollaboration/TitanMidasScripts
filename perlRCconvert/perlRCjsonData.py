#!/home/mpet/local/bin/python2.7
import sys
sys.path.append('/home/mpet/Aaron/perlRCdb/')

#import MidasToEvaSubClass as MidasToEvaSDA
from midas2eva import SDA
from collections import Counter
import json
import extractFromPerlRCLog as exprc


def getjson(filename):
    #M2E = MidasToEvaSDA.SDA(filename)
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
        for j in hist:
            jsonData.append({'f': i % numFreq, 'c': j, 'N': hist[j]})

    return jsonData


def getAllJson():
    prc = exprc.extractFromPerlRCLog()

    prc.get_last_scan()
    prc.last_scan_runs()
    prc.last_scan_filenames()
    files = prc.runFilenames

    date = prc.last_scan_date()

    files = [prc.datapath + date + '/' + f for f in files]

    data = [getjson(f) for f in files]

    scanvals = prc.last_scan_values()
    scanvar = prc.last_scan_variable()

    for d, y in zip(data, scanvals):
        for x in d:
            x['scanval'] = float(y)
            x['scanvar'] = scanvar
            x['scan'] = 1

    if prc.last_scan_type() == "Scan2D":
        for d in data[1::2]:
            for x in d:
                x['scan'] = 2

    return flatten(data)


def dumpJson():
    data = getAllJson()
    with open('/home/mpet/online/custom/jsondump.json', 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '))


def flatten(a, result=[]):
    for elem in a:
        if isinstance(elem, list):
            flatten(elem, result)
        else:
            result.append(elem)

    return result

if __name__ == "__main__":
    dumpJson()
