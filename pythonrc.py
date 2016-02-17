#!/usr/bin/python

import pythonmidas.pythonmidas as Midas
import re
#from numpy import *
import numpy as np
import datetime
import sys
import time

ControlVarPath = "/PerlRC/ControlVariables/"
TunePath = "/PerlRC/Tunes/"
RunControlPath = "/PerlRC/RunControl/"
Scan1DPath = RunControlPath + "Scan1D/"
Scan2DPath = RunControlPath + "Scan2D/"
TuneSwitchPath = RunControlPath + "TuneSwitch/"
RCActive = RunControlPath + "RCActive"
LogFile = "/titan/data1/mpet/PerlRC.log"


def StringToList(varStr, splitChar=";"):
    """
    StringToList(x,SplitChar=";") takes a string,
    splits it at the given 'SplitChar'
    and strips any extra white space. Returns a list.
    """
    return [x.strip() for x in varStr.split(splitChar)]
    #return map(lambda x: x.strip(), varStr.split(";"))


def StringListToFloatList(strList):
    """
    StringListToFloatList(strList) takes a list of strings and converts
    each element into a float.

    TRAP VOLTAGE SETTINGS:

    Special care is taken if the value is a trap voltage setting, as
    one needs to split the variable on back-to-back ")(" parentheses.
    This function detects if the value is a trap voltage by checking if
    the first and last non-whitespace characters are a "(" and ")",
    respectively.
    The trap values are then converted into a numpy array, through the use
    of an 'eval'. Python detects if someone tried to put code into the
    array, so it should be safe to use this to convert the 'tuple' of
    trap values into something we can do a calculation with.
    """

    print strList

    templist = []
    for x in strList:
        # Check if trap variable by seeing if there are () in the variable.
        # If true, create a numpy array to hold the object.
        # Convert to a float otherwise
        if re.search("^\s*\(.+\)\s*$", x):
            # split on ")(" (back to back parentheses), allowing for
            # any amount of white space in between.
            #templist = np.array(map(eval, re.sub("\)\s*\(",
            #                                     ");(", x).split(';')))
            templist.append(np.array(map(eval, re.sub("\)\s*\(",
                                                      ");(", x).split(';'))))
        else:
            templist.append(float(x))
    return templist


def GetVariableStepSize(varStart, varStop, nVarStep):
    """
    GetVariableStepSize(varListStart,varListStop,nVarStep) returns a list
    with the variable step size based on the given lists. Lists must be floats
    or ints. Note that the lists must be the same length (function does not
    check for this).
    If the number of steps is 1, then the function will return varStart.
    """
    if nVarStep > 1:
        return (varStop - varStart) / (nVarStep - 1.)
    else:
        return varStart


def NextVariableSetPoint(VarStart, VarStop, nVarStep, currStep):
    return (VarStart
            + GetVariableStepSize(VarStart, VarStop, nVarStep) * currStep)


def GetVarName(perlVarName):
    """
    Given the PerlRC variable name, return the path to the location of the ODB
    variable.
    *** Essentially return the value associated with the variable in the
    /PerlRC/ControlVariable directory.
    """
    global ControlVarPath
    return Midas.varget(ControlVarPath + perlVarName)


def MidasSetVar(varPath, varValue):
    """
    Wrapper for pythonmidas.setvar(key,val).
    Deals with some special cases in in ODB.
    """

    varValue = ConvertValueToString(varValue)
    print varValue
    try:
        Midas.varset(varPath, varValue)
    except Midas.FailedCommand as e:
        Midas.sendmessage('pythonrc', e.value)
        raise Exception
    except Midas.KeyNotFound as e:
        Midas.sendmessage('pythonrc', e.value)
        raise Exception


def ConvertValueToString(val):
    """
    Convert a value back into a form suitable for MIDAS.

    TRAP VOLTAGE SETTING:
        If the value is an array, then a trap value is being converted.
        To convert it, we check to see if the value has a length, and
        then construct the string.

        If any of these steps fail, it is a normal value, so we just
        convert to a string normally.
    """
    # if the value is an array, recreate the value string for MIDAS, otherwise
    # just directly convert the value to a string.
    try:
        len(val)
        val = " ".join("(%d" % x + ",%.4f)" % y for x, y in map(tuple, val))
    except:
        val = str(val)

    return val


def ChangeTune(tuneName):
    """
    Change all the MIDAS values in the given tune path.
    """
    for var, val in Midas.dirlist(TunePath + tuneName):
        MidasSetVar(GetVarName(var), val)
    Midas.sendmessage("pythonrc", "Changed tune to: " + tuneName)


def Scan1D():
    """
    Scan1D() does a 1D scan
    """
    Scan1Dn = int(Midas.varget(RunControlPath + "RCTotalRuns"))
    Scan1Dcurrn = int(Midas.varget(RunControlPath + "RCCurrentRun"))

    # Update the current scan number in the RunControlPath
    Scan1Dcurrn += 1
    if Scan1Dcurrn > Scan1Dn:
        Scan1Dcurrn = 1
    Midas.varset(RunControlPath + "RCCurrentRun", Scan1Dcurrn)
    Scan1Dcurrn -= 1  # To get the right scan range.

    # Get the varibales to be scanned, and the start and stop values
    Variables = Midas.varget(Scan1DPath + "Variables")
    Start = Midas.varget(Scan1DPath + "VarStart")
    Stop = Midas.varget(Scan1DPath + "VarStop")
    # Don't need the totalsteps or currentstep for 1D scan
    #n = Midas.varget(Scan2DPath + "VarSteps")
    #currn = Midas.varget(Scan2DPath + "VarCurrentStep")

    print Variables

    Variables, Start, Stop = map(StringToList, [Variables, Start, Stop])
    Start, Stop = map(StringListToFloatList, [Start, Stop])

    NextVariableStep = map(lambda x, y:
                           NextVariableSetPoint(x, y, Scan1Dn, Scan1Dcurrn),
                           Start, Stop)

    returnstr = ""
    for var, val in zip(Variables, NextVariableStep):
        print var, val
        MidasSetVar(GetVarName(var), val)
        returnstr += var + "=" + ConvertValueToString(val) + ";"

    return returnstr


def Scan2D():
    """
    Scan2D() does a 2D scan
    """
    Scan2Dn = int(Midas.varget(RunControlPath + "RCTotalRuns"))
    Scan2Dcurrn = int(Midas.varget(RunControlPath + "RCCurrentRun"))

    Scan2Dcurrn += 1
    if Scan2Dcurrn > Scan2Dn:
        Scan2Dcurrn = 1
    Midas.varset(RunControlPath + "RCCurrentRun", Scan2Dcurrn)

    # Lots of variables in a 2D scan, so list them:
    dirKeys = ["Variables1", "Var1Start", "Var1Stop", "Var1Steps",
               "Var1CurrentStep", "Variables2", "Var2Start", "Var2Stop",
               "Var2Steps", "Var2CurrentStep"]
    # Get the values of the variables:
    Variables1, Start1, Stop1, n1, currn1, \
        Variables2, Start2, Stop2, n2, currn2 = \
        [Midas.varget(Scan2DPath + x) for x in dirKeys]
    # Convert into a list
    Variables1, Start1, Stop1, Variables2, Start2, Stop2 = \
        map(StringToList, [Variables1, Start1,
                           Stop1, Variables2, Start2, Stop2])
    # Convert into floats
    Start1, Stop1, Start2, Stop2 = \
        map(StringListToFloatList, [Start1, Stop1, Start2, Stop2])

    # Check that currn's are correct
    currn1 = int(currn1)
    n1 = int(n1)
    currn2 = int(currn2)
    n2 = int(n2)

    # Update the 2D scan counters.
    # Ensure that if either currn1 or currn2 are at their max values that
    # they are reset back to 1.
    currn2 += 1
    if currn2 > n2:
        currn2 = 1

        currn1 += 1
        if currn1 > n1:
            currn1 = 1
    Midas.varset(Scan2DPath + "Var1CurrentStep", currn1)
    Midas.varset(Scan2DPath + "Var2CurrentStep", currn2)
    # de-increment to calculate the scan value
    currn1 -= 1
    currn2 -= 1

    NextVariableStep1 = map(lambda x, y:
                            NextVariableSetPoint(x, y, n1, currn1),
                            Start1, Stop1)
    NextVariableStep2 = map(lambda x, y:
                            NextVariableSetPoint(x, y, n2, currn2),
                            Start2, Stop2)

    # Write out the list of variables
    # Each variable is separated by a ';', while the 2D scans
    # are separated by ';;'
    returnstr = ""
    for var, val in zip(Variables1, NextVariableStep1):
        print var, val
        MidasSetVar(GetVarName(var), val)
        returnstr += var + "=" + ConvertValueToString(val) + ";"

    returnstr += ";"
    for var, val in zip(Variables2, NextVariableStep2):
        print var, val
        MidasSetVar(GetVarName(var), val)
        returnstr += var + "=" + ConvertValueToString(val) + ";"

    return returnstr


def TuneSwitch():
    """
    TuneSwitch() switches bewteen the listed tunes.
    """
    RunN = int(Midas.varget(RunControlPath + "RCTotalRuns"))
    Runcurrn = int(Midas.varget(RunControlPath + "RCCurrentRun"))

    Runcurrn += 1
    if Runcurrn > RunN:
        Runcurrn = 1
    Midas.varset(RunControlPath + "RCCurrentRun", Runcurrn)

    #Tunes, currn, CurrentTune = zip(*Midas.dirlist(TuneSwitchPath))[1]
    Tunes = Midas.varget(TuneSwitchPath + "TunesList")
    currn = Midas.varget(TuneSwitchPath + "CurrentTuneIndex")
    #CurrentTune = Midas.varget(TuneSwitchPath + "CurrentTuneName")

    currn = int(currn)
    Tunes = StringToList(Tunes)

    currn += 1
    if currn > len(Tunes):
        currn = 1
    Midas.varset(TuneSwitchPath + "CurrentTuneIndex", currn)
    currn -= 1

    ChangeTune(Tunes[currn])
    Midas.varset(TuneSwitchPath + "CurrentTuneName", Tunes[currn])
    return "Tune is \"" + Tunes[currn] + "\""


def GetTime():
    """
    GetTime() returns the current date and time.
    The format is H:M:S dayName monthName dayNumber Year.
    Example 14:36:16 Wed Aug 21 2013
    """
    return datetime.datetime.now().strftime("%X, %a %b %d, %Y")


def LogScanStart():
    """
    Writes information to the PerlRC.log file at the beginning of a scan.
    """

    CurrentScan = int(Midas.varget(RunControlPath + "RCCurrentRun"))

    if CurrentScan == 1:
        CurrentTime = GetTime()
        CurrentTune = Midas.varget(RunControlPath +
                                   "TuneSwitch/CurrentTuneName")
        ScanType = Midas.varget(RunControlPath + "RCType")
        NRuns = Midas.varget(RunControlPath + "RCTotalRuns")

        with open(LogFile, 'a') as myfile:
            myfile.write("=== NEW PerlRC scan at " + CurrentTime + " ===\n")
            myfile.write("=== Scan type is \"" + ScanType + "\"; "
                         + "Current Tune is \"" + CurrentTune + "\" ===\n")
            myfile.write("=== Number of runs in this scan is " +
                         NRuns + " ===\n")


def LogScanStop():
    """
    Write iformation to the PerlRC.log file at the end of a scan.
    """

    CurrentScan = int(Midas.varget(RunControlPath + "RCCurrentRun"))
    NRuns = int(Midas.varget(RunControlPath + "RCTotalRuns"))

    if CurrentScan == NRuns:
        with open(LogFile, 'a') as myfile:
            myfile.write("===             Finished PerlRC scan" +
                         "===\n")
            myfile.write("====================================" +
                         "================\n")

        # Deactivate the Scans
        Midas.varset(RCActive, 'n')


def LogScanVarStep(ScanString=""):
    """
    Write the ScanString to PerlRC.log.
    """

    CurrentRun = int(Midas.varget("/Runinfo/Run number")) + 1
    CurrentRun = str(CurrentRun)

    with open(LogFile, 'a') as myfile:
        myfile.write("<Run #" + CurrentRun + "> " + ScanString + "\n")


def LogScanError():
    """
    Error occurred. Write message to PerlRC.log.
    """

    with open(LogFile, 'a') as myfile:
        myfile.write("!!!#### Aborting scan! ####!!!\n")


def LogSwitchedTune(tune="", error=False):
    """
    Write tune was switched to 'tune' in PerlRC.log.
    """

    if error:
        with open(LogFile, 'a') as myfile:
            CurrentTime = GetTime()
            myfile.write("ERROR trying to SwitchToTune "
                         + tune + " at " + CurrentTime + "\n")
    else:
        with open(LogFile, 'a') as myfile:
            CurrentTime = GetTime()
            myfile.write("SwitchedToTune " + tune +
                         " at " + CurrentTime + "\n")


def main():
    StartScan = Midas.varget(RCActive)
    try:  # If called from the command line parse the arguements
        print sys.argv
        if len(sys.argv) == 2:
            # Start a PerlRC scan
            if sys.argv[1] == "start":
                Midas.varset(RCActive, 'y')
                StartScan = 'y'
            # Stop a PerlRC scan
            if sys.argv[1] == "stop":
                Midas.varset(RCActive, 'n')
                StartScan = 'n'
        # Change to a tune
        elif len(sys.argv) == 3 and sys.argv[1] == "tune":
            try:
                ChangeTune(sys.argv[2])
                LogSwitchedTune(sys.argv[2])
            except:
                LogSwitchedTune(sys.argv[2], True)
    except:  # calling it as a module, so ignore the stuff above
        pass

    # If we're doing a PerlRC scan, do what's in the ODB.
    if StartScan == 'y':
        ScanFuncs = {"SCAN1D": Scan1D,
                     "SCAN2D": Scan2D,
                     "TUNESWITCH": TuneSwitch}

        # Get the scan type and convert to uppercase
        ScanType = Midas.varget(RunControlPath + "RCType").upper()
        try:
            # call scan function based on the ScanType
            scanoutput = ScanFuncs[ScanType]()
            # Write some info to the log file
            # LogScanStart and LogScanStop only write something
            # if it's the beginning or end of a PerlRC scan.
            LogScanStart()
            LogScanVarStep(scanoutput)
            LogScanStop()

            # Sleep for a second so that scepics can update
            # the values
            time.sleep(1)
            Midas.startrun()
        except:
            # Error occurred. Stop future runs, and write an error message
            Midas.varset(RCActive, 'n')
            LogScanError()
            Midas.sendmessage("pythonrc", "There was a problem. " +
                              "Please check input variables and values, " +
                              "and the message log for more info.")


if __name__ == "__main__":  # pragma: no cover
    main()
