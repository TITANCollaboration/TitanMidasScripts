#!/bin/bash
#

#echo $MIDAS_EXPT_NAME

# Get name of last written file
path=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Data dir"'`
path=`echo $path | awk '{print $3}'`
path='/titan/data1/mpet'
#echo $path
filename=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Channels/0/Settings/Current Filename"'`
filename=`echo $filename | awk '{print $3}'`
#echo $filename

# Check to see if the data was being written
wdata=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Logger/Write data"'`
wdata=`echo $wdata | awk '{print $3}'`
#echo $wdata

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
#echo $convert

#check to see if Ramsey mode:
Ramsey=`odb -e $MIDAS_EXPT_NAME -c 'ls "/Equipment/TITAN_ACQ/ppg cycle/"'`
Ramsey=`echo $Ramsey | grep QUAD3`

if [ "$wdata" == "n" ]
then
   # data was not written
  # echo Data was not written.
   exit
fi
#python /home/mpet/Aaron/TitanMidasScripts/getFreqC.py
# Don't convert when PerlRC is running, unless it's a tune switch
#if [ "$PRC" == "y" && "$TuneSwitch" != "TuneSwitch" ] # PerlRC running, so don't convert #echo PerlRC running
   #exit
#fi

if [ "$convert" == "n" ]
then
   # Convert checkbox now clicked.
   #echo User does not wish to convert.
   exit
fi

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
#ssh mpet@lxmpet "m2e -v$RFAmp -d/titan/data1/mpet/evafiles/  $filename"
# We don't need the RFAmp anymore, so ignore it
#`m2e -v$RFAmp -d/titan/data1/mpet/evafiles/  $filename`
result=`m2e -d/titan/data1/mpet/evafiles/ $filename`
message="Done conversion of file: $filename"
result=`odb -e $MIDAS_EXPT_NAME -c "msg 'at_run_stop'  '$message' "`
