import calcFreq.calcFreq as calcfreq
import pythonmidas.pythonmidas as Midas
import numpy as np
import re
import sys

CF = calcfreq.calcFreq()
CF.getReference()


def checkInput(name):
    names = CF.splitInput(name)

    passes = True

    elemList = np.hstack(([re.findall('\\d+', x) for x in names],
                          [re.findall('\\D+', x) for x in names]))
    try:
        [float(x[0]) * CF.getAtomicMass(x[0] + x[2] + x[1]) for x in elemList]
    except IndexError:
        print "Element in input", name, "does not exist in AME table."
        #passes = False
        Midas.sendmessage("DipoleCalculator", "Element in input " + name +
                          " does not exist in AME table.")

    return passes


#####################
# Start the program
#####################

if __name__ == "__main__":
    #args = sys.argv

    #if len(args) > 1 and args[1] == "dipole":
        names = Midas.varget("/Experiment/Variables/Contaminants/" +
                             "Contaminant List")

        reducedCyclotron = CF.dipole_frequencies(names)
        cyclotron = CF.cyclotron_frequencies(names)

        Midas.varset("/Experiment/Variables/Contaminants/Contaminant FreqPlus",
                     ", ".join(["%0.3f" % x for x in reducedCyclotron]))
        Midas.varset("/Experiment/Variables/Contaminants/Contaminant FreqC",
                     ", ".join(["%0.3f" % x for x in cyclotron]))
