# TITAN Midas Scripts

Here are a collection of scripts that are used to simplify life for the TITAN experiment.

# Required Python Packages

Several python packages are required to run these scripts:

* Afgcontrol (https://github.com/aarongallant/Afgcontrol)
* CalcFreq (https://github.com/aarongallant/CalcFreq)
* Pythonmidas (https://github.com/aarongallant/Pythonmidas)
* MidasToEva (https://github.com/aarongallant/MidasToEva)

These can be downloaded into a directory using:

    git clone <http://path-to-repository>
    cd into-repository
    python2.6 setup.py install --prefix=$HOME/.local
    python2.7 setup.py install --prefix=$HOME/.local

This will install the python package into the ~/.local directory.

IMPORTANT: Inorder to have these packages work properly on both titan01 and lxmpet
you must run the command once on titan01 (python2.6), and a second time on lxmpet
using python2.7.

# General Information

Each script is generally tied to one "button" on the MIDAS status page, and its
function can be derived from the name of the script. For example, the scirpt
"afgOnOff.py" toggles the state of the quadrupole AFG, while the scirpt
"afgDipoleOnOff.py" toggles the state of the swift/dipole AFG.

The current scripts, and their functions are:

* afgDipoleOnOff.py: Toggles the state of the ouput channel of the dipole afg
* afgOnOff.py: Toggles the statue of the output channel of the quadrupole afg
* afgSetDipoleFreqList.py: Programs the frequnecy list to the dipole afg
* afgSetFreqList.py: Programs the frequency list to the quadrupole afg
* convertOnRunStop.sh: Converts a MIDAS file to an EVA file at the end of a run
* getFreqC.py: Calculates the cyclotron frequency for a given species
* m2e.py: Converts MIDAS file to EVA file
* midasOnStart.sh: Commands that are run prior to a run start
* midasOnStop.sh: Commands that are run at the end of a run
* midasQuadCycle.sh: Change the PPG cycle to a normal one-pulse excitation
* midasRamseyCycle.sh: Change the PPG cycle to a Ramsey two-pulse excitation
* perlrc.sh: Calls pyhtonrc.py. Kept for testing between perlrc and pythonrc
* pythonrc.py: Re-write of perlrc to python. Allows scanning of beamline elements

# Alarm Scripts

MIDAS allows one to set certian alarm conditions (vacuum readbacks, current settings, voltage settings, etc.), and to execute a script to handle the alarm.

Generally the MIDAS alarm condition allows for simple commands to be executed, however, it is possible to use more complicated script files.

The current alarm scripts are:

* /Alarms/MpetVacuum/MpetVacuumEmail.py: If the vacuum in MPET trips, send an email to MPET members to alert to the vacuum condition.

# Cycle Time

These are scripts that run the tri_config program to generate the timings for the current ppg settings. It uses the files generated to determine how long a given run will take.

This script is implemented as a button on the MIDAS page.
