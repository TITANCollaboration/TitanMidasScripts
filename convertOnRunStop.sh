#!/bin/bash
#

# Get name of last written file
path=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Data dir"'`
path=`echo $path | awk '{print $3}'`
echo "Data Dir: " $path
filename=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Channels/0/Settings/Current Filename"'`
filename=`echo $filename | awk '{print $3}'`
echo "Filename: " $filename

# Check to see if the data was being written
wdata=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Write data"'`
wdata=`echo $wdata | awk '{print $3}'`
echo "Write Data?" $wdata

# Check to make sure this isn't a PerlRC run
PRC=`odb -e $MIDAS_EXPT_NAME -c 'ls "/PerlRC/RunControl/RCActive"'`
PRC=`echo $PRC | awk '{print $2}'`
#echo $PRC

#check to see if this is a TuneSwitch
TuneSwitch=`odb -e $MIDAS_EXPT_NAME -c 'ls "/PerlRC/RunControl/RCType"'`
TuneSwitch=`echo $TuneSwitch | awk '{print $2}'`

# Check to see if the user wants to convert
convert=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Experiment/Variables/Convert File"'`
convert=`echo $convert | awk '{print $3}'`
echo "Convert file?" $convert

#check to see if Ramsey mode:
Ramsey=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Equipment/TITAN_ACQ/ppg cycle/"'`
Ramsey=`echo $Ramsey | grep QUAD3`

# Check to see if a file was written
if [ "$wdata" == "n" ]
then
   # data was not written
   echo Data was not written.
   exit
fi

# Check to see if user wants to convert the file
if [ "$convert" == "n" ]
then
   # Convert checkbox now clicked.
   echo User does not wish to convert.
   exit
fi

# Get the RF amplitude, and correct for Ramsey scheme
RFAmp=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Experiment/Variables/MPETRFAmp"'`
RFAmp=`echo $RFAmp | awk '{print $2}'`
if [ "$Ramsey" == "transition_QUAD3" ]
then
   RFAmp=`echo "$RFAmp * 2.0" | bc` # double RF amplitude so that EVA reads it correctly
fi

# Construct absolute path to the midas file
filename=$path"/"$filename
#echo Filename to convert: $filename

# convert the file on lxmpet
result=`/home/mpet/local/bin/python2.7 /home/mpet/local/scripts/m2e.py -d/titan/data1/mpet/evafiles/ $filename 2>&1`
error=$?
echo $result
if [ "$error" == "0" ]
then
	message="Done conversion of file: $filename"
else
	message="Error converting file: $filename Please check if file exists, or if there is a cycle number problem"
fi
echo $message
odbmessage=`odb -e $MIDAS_EXPT_NAME -c "msg 'at_run_stop'  '$message' "`
