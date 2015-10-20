#!/bin/bash
#

CycleTime() {
	FringeTime=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD2 -c ls | grep 'time offset (ms)' | awk '{print $4}'`
	WaitTime=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD3 -c ls | grep 'time offset (ms)' | awk '{print $4}'`

	CycleTime=`echo 2*$FringeTime+$WaitTime | bc`

	echo $CycleTime
}

# Get number of DIPOLE transitions:
numDPL=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep transition_DPL | wc | awk '{print $1}'`

# Get number of QUAD transitions:
numQUAD=`odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c ls | grep transition_QUAD | wc | awk '{print $1}'`

# Output useful stuff:
echo "Number of Dipole transitions" $numDPL
echo "Number of Quad transitions" $numQUAD

if [ $numQUAD -eq 2 ] # Already set to Quad excitation
then
	echo "Setting is already Quadrupole excitation."
	message="Cycle is already set for Quadrupole excitations. No changes made."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Quad'  '$message' "
elif [ $numQUAD -eq 4 ] # Was set to Ramsey
then
	echo "Setting is NOT Quadrupole excitation."

	CycleLength=$(CycleTime)
	
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "del transition_QUAD3"
	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle -c "del transition_QUAD4"

	odbedit -d /Experiment/Edit\ on\ Start -c "del 'Quad Waiting Time (ms)'"
	odbedit -d /Experiment/Edit\ on\ Start -c "del 'Quad RF Time2 (ms)'"

	odbedit -d /Equipment/TITAN_ACQ/ppg\ cycle/transition_QUAD2 -c "set 'time offset (ms)' $CycleLength"

	message="Cycle is changed for Quadrupole excitations. Please double check transition times."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Quad'  '$message' "
else
	echo "Error. Cycle is in unknown setting. Please Fix. No changes made."
	message="Error: Unknown cycle. Please check ppg cycle. No changes made."
	odb -e $MIDAS_EXPT_NAME -c "msg 'Change2Quad'  '$message' "
fi
