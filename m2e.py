#!/home/mpet/local/bin/python2.7
######!/usr/bin/python

from optparse import OptionParser
#import MidasToEva7 as MidasToEva
import midas2eva as MidasToEva

def main():
  parser=OptionParser()
  parser = OptionParser(usage="usage: %prog [options] <MidasFileName>")
  parser.add_option("-e","--ElementSymbol",dest="elem",default=None,
    help="Chemical denomination, i.e. 1Li6, or 1C12. Required.")
  parser.add_option("-z","--Charge",dest="z",default=None,
    help="Ion charge.")
  parser.add_option("-v","--RFAmplitude",dest="rfamp",default=None,
    help="RF amplitude in Volts. Required.")
  parser.add_option("-x","--RFTime",dest="rftime",default=None,
    help="RF excitation time in seconds. Required")
  parser.add_option("-b","--BinWidth",dest="binwidth",default=0.2,
    help="TDC binning width, in microseconds. Default=0.2us")
  parser.add_option("-i","--BinNumber",dest="nbins",default=None,
    help="Number of TDC bins.")
  parser.add_option("-s","--StartFrequency",dest="startf",default=None,
    help="Value of the start frequency, overrides MIDAS value")
  parser.add_option("-t","--StopFrequency",dest="stopf",default=None,
    help="Value of the stop frequency, overrides MIDAS value")
  parser.add_option("-a","--StartTime",dest="startt",default=None,
    help="Value of the start time, overrides MIDAS value")
  parser.add_option("-o","--StopTime",dest="stopt",default=None,
    help="Value of the stop time, overrides MIDAS value")
  parser.add_option("-f","--NFrequencies",dest="nfreq",default=None,
    help="Number of frequency steps, overrides MIDAS value")
  parser.add_option("-d","--OutputDir",dest="outdir",
    default="/triumfcs/trshare/titan/MPET/Data/",
    help="Output directory for EVA file")
  parser.add_option("-r","--midFileVersion",dest="version",default=2,
    help="Version of the stored .mid file: 1=original;"
	" 2=double loop (dec07)")

  opts, args = parser.parse_args()
  if len(args) != 1:
    parser.error("This program needs a single argument: the name of the MIDAS file to process! Try again")
  #if opts.z==None:
  #  parser.error("You HAVE to specify the charge state of the studied ion (-z<Z>)")
  #if opts.elem==None:
  #  parser.error("You HAVE to specify the chemical abbreviation of the studied ion (-e<Elem>)")
  #if opts.rfamp==None:
  #  parser.error("You HAVE to supply rf amplitude (-v<Volt>)")
  #if opts.rftime==None:
  #  parser.error("You HAVE to specify the rf time (-x<Time>)")

  test=MidasToEva.MidasToEva(args[0])
  test.versionMID=opts.version
  test.extractXML()
  test.getStartFreq(opts.startf)
  test.getStopFreq(opts.stopf)
  test.getStartTime(opts.startt)
  test.getEndTime(opts.stopt)
  test.getNumFreqSteps(opts.nfreq)
  test.getNumCycles()
  test.getCycleTime()
  test.getAmplitude(opts.rfamp)
  test.getElem(opts.elem)
  test.getZ(opts.z)
  test.getRFTime(opts.rftime)
  test.collectMdumpData()
  test.reorganizeMdumpData()
  test.setTdcGateWidth(opts.nbins)
  #test.binMdumpData(opts.binwidth,opts.nbins)
  test.binMdumpData(opts.binwidth, test.tdcTime)
  test.writeEvaFile(opts.elem,opts.z,opts.rfamp,opts.rftime,
    opts.outdir)
  #test.writeErrorData()
  test.writePosData()

if __name__ == "__main__":
    main()
