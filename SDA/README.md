# Simplified Data Analysis

This is a collection of conversion scripts and MATLAB plotting routines to plot data from PerlRC scans.

# Analyzing the most recent PerlRC scan

After running a PerlRC scan, to "analyze" the files and "plot" the results, you must:

* Press the "Convert PerlRC" button on the MIDAS status page.
* Press the "PRCView" button to see the scan results in the brower.

'''NOTE''': This will only convert the data in the most recent PerlRC scan.
If you want to plot past data then you need to follow the directions in "Plotting Older Scans".

It may be that you need to change the MCA range for your PerlRC scan.
One instance where this may be required is when changing from SCI to HCI.

The MCA range is set in the file "/home/mpet/local/scripts/SDA/simplifiedScan1Danalysis_input_AG.dat".
Simply open the file in a text editor "nano, pico, nedit, vim, emacs, etc.) and set the range to appropriate values. 
Then, re-convert the files with the new MCA range by pressing the "Convert PerlRC" button.

## PRCView Page Not Working

If the PRCView page is not working, then you can plot the PerlRC scan in MATLAB.
First, convert the last PerlRC scan by pressing the "Convert PerlRC" button.
Then, in a terminal, enter the following commands: 
* cd ~/local/scripts/SDA/
* matlab &

In MATLAB:
* simplifiedScan1DanalysisPlottingWithIonsVsF_AG

If the PerlRC scan was a 2D scan, also run the command:
* analysis2Dscan2values

MATLAB will open a plotting window with the results from the PerlRC scan.

## Plotting Older Scans

If you want to replot an older scan, you can do this by opening the PerlRC.log file.
This file is located in "/data1/mpet".

Find the scan you wish to plot, and copy and paste these lines to the end of the file.
Then follow the steps above to plot the scan results.

# General Operation

## Theory of Operation

The idea of "simplified data analysis" is to convert the MIDAS files generated in a PerlRC scan, and plot
the results.

* simplifiedScan1Danalysis_AG.sh
 * this script reads the entries in "simplifiedScan1Danalysis_input_AG.dat" and generates the plot data
based on the files and settings listed.
* simplifiedScan1Danalysis_input_AG.dat
 * Contains the settings to be used when analysing the PerlRC data (MCA range, etc).
 * Constains a list of the variable settings, and run number of the corresponding MIDAS run. This is copied
from PerlRC.log
* s1da_makeInputFiles_AG.c
 * C source code to generated the input files for plotting in MATLAB
 * Generates fileListPlotTOF.dat and fileListPlotPos.dat
* m2e_se.sh
 * A custom version of the m2e.py script that's used to convert the MIDAS files to something useful for the
simplified data analysis
* m2eseries_se.sh
 * a generated file that contains a list of all the m2e_se.sh commands to convert all of the MIDAS files 
listed in simplifiedScan1Danalysis_input_AG.dat
* simplifiedScan1Danalysis_AG.sh
 * Script to run all of the above
 * This is the only one we need to run
* simplifiedScan1DanalysisPlottingWithIonsVsF_AG.m
 * MATLAB routines for plotting the generated data from above
* analysis2Dscan2values.m
 * If the PerlRC scan was 2D, this script contains functions for plotting the "2D" data

## Manually Entering Scan Values

The most basic way to use the scripts here is to manually enter the data from a PerlRC scan into the 
simplifiedScan1Danalysis_input_AG.dat file (cutting and pasting), and updating the control variables. In
this section we describe how this is done, along with a working example.

Below is an example input file:

    convert Midas files?
    y
    m2e default:
    ./m2e_se.sh -e1Na23 -z1 -x0.100 -v0.271 /titan/data5/mpet/20150904/
    MCA Range:
    21 51
    Plot Indiviudal?
    n
    Plot Positions?
    n
    Scan2D Value:
    <Run #264997> TOF gate (ms)=0.024;;Centre Frequency (Hz)=1000000;
    <Run #264998> TOF gate (ms)=0.024;;Centre Frequency (Hz)=5220513.5;
    <Run #264999> TOF gate (ms)=0.0242;;Centre Frequency (Hz)=1000000;
    <Run #265000> TOF gate (ms)=0.0242;;Centre Frequency (Hz)=5220513.5;
    <Run #265001> TOF gate (ms)=0.0244;;Centre Frequency (Hz)=1000000;
    <Run #265002> TOF gate (ms)=0.0244;;Centre Frequency (Hz)=5220513.5;
    <Run #265003> TOF gate (ms)=0.0246;;Centre Frequency (Hz)=1000000;
    <Run #265004> TOF gate (ms)=0.0246;;Centre Frequency (Hz)=5220513.5;
    <Run #265005> TOF gate (ms)=0.0248;;Centre Frequency (Hz)=1000000;
    <Run #265006> TOF gate (ms)=0.0248;;Centre Frequency (Hz)=5220513.5;
    <Run #265007> TOF gate (ms)=0.025;;Centre Frequency (Hz)=1000000;
    <Run #265008> TOF gate (ms)=0.025;;Centre Frequency (Hz)=5220513.5;
    <Run #265009> TOF gate (ms)=0.0252;;Centre Frequency (Hz)=1000000;
    <Run #265010> TOF gate (ms)=0.0252;;Centre Frequency (Hz)=5220513.5;
    <Run #265011> TOF gate (ms)=0.0254;;Centre Frequency (Hz)=1000000;
    <Run #265012> TOF gate (ms)=0.0254;;Centre Frequency (Hz)=5220513.5;
    <Run #265013> TOF gate (ms)=0.0256;;Centre Frequency (Hz)=1000000;
    <Run #265014> TOF gate (ms)=0.0256;;Centre Frequency (Hz)=5220513.5;
    <Run #265015> TOF gate (ms)=0.0258;;Centre Frequency (Hz)=1000000;
    <Run #265016> TOF gate (ms)=0.0258;;Centre Frequency (Hz)=5220513.5;
    <Run #265017> TOF gate (ms)=0.026;;Centre Frequency (Hz)=1000000;
    <Run #265018> TOF gate (ms)=0.026;;Centre Frequency (Hz)=5220513.5;
    end
