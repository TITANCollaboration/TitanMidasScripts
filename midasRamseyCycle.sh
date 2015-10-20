#!/bin/bash
#

CalcRamseyFringe() {
	QuadTime=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "ls 'transition_QUAD2/time offset (ms)'" | awk '{print $4}'`
	FringeTime=`echo $QuadTime/5 | bc`

	WaitTime=`echo $QuadTime-2*$FringeTime | bc`

	# echo $QuadTime $FringeTime $WaitTime
	echo $FringeTime $WaitTime
}

# Get number of DIPOLE transitions:
numDPL=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep transition_DPL | wc | awk '{print $1}'`

# Get number of QUAD transitions:
numQUAD=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep transition_QUAD | wc | awk '{print $1}'`

# Output useful stuff:
echo "Number of Dipole transitions" $numDPL
echo "Number of Quad transitions" $numQUAD

if [ $numQUAD -eq 4 ] # Was set to Ramsey
then
	echo "Setting is NOT Quadrupole excitation."
	message="Cycle is already set for Ramsey exitations. No changes made."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Ramsey'  '$message' "
elif [ $numQUAD -eq 2 ] # was set to Quad
then
	echo "Setting is Quadrupole excitation cycle. Changing now..."
	
	# Get position of last Quad transition
	
	lastQUADPos=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep -n transition_QUAD | sed 's/\:/ /g' | tail -1 | awk '{print $1}'`
	lastEOSpos=`odbedit -d /Experiment/Edit\ on\ Start -c ls | grep -n Quad\ RF\ Time\ \(ms\) | sed 's/\:/ /g' | tail -1 | awk '{print $1}'`
	lastEOSpos=`echo \($lastEOSpos+1\)/2 | bc`
	echo $lastEOSpos
	
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "copy transition_QUAD2 transition_QUAD3"
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "move transition_QUAD3 $lastQUADPos"

	odbedit -d /Experiment/Edit\ on\ Start/ -c "ln '/Equipment/TITAN_ACQ/ppg cycle/transition_QUAD3/time offset (ms)' 'Quad Waiting Time (ms)'"
	odbedit -d /Experiment/Edit\ on\ Start/ -c "move 'Quad Waiting Time (ms)' $lastEOSpos"
	
	lastQUADPos=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep -n transition_QUAD | sed 's/\:/ /g' | tail -1 | awk '{print $1}'`
	
	lastEOSpos=`odbedit -d /Experiment/Edit\ on\ Start -c ls | grep -n 'Quad Waiting Time (ms)' | sed 's/\:/ /g' | tail -1 | awk '{print $1}'`
	lastEOSpos=`echo \($lastEOSpos+1\)/2 | bc`

	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "copy transition_QUAD3 transition_QUAD4"
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "move transition_QUAD4 $lastQUADPos"

	odbedit -d /Experiment/Edit\ on\ Start/ -c "ln '/Equipment/TITAN_ACQ/ppg cycle/transition_QUAD4/time offset (ms)' 'Quad RF Time2 (ms)'"
	odbedit -d /Experiment/Edit\ on\ Start/ -c "move 'Quad RF Time2 (ms)' $lastEOSpos"

	RamseyTimes=$(CalcRamseyFringe)
	FringeTime=`echo $RamseyTimes | awk '{print $1}'`
	WaitTime=`echo $RamseyTimes | awk '{print $2}'`

	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD2 -c "set 'time offset (ms)' $FringeTime"
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD3 -c "set 'time offset (ms)' $WaitTime"
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD4 -c "set 'time offset (ms)' $FringeTime"
	
	message="Cycle is changed for Ramsey excitations. Please check transition times."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Ramsey'  '$message' "
else
	echo "Error. Cycle is in unknown setting. Please Fix. No changes made."
	message="Error: Unknown cycle. Please check ppg cycle. No changes made."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Ramsey'  '$message' "
fi
