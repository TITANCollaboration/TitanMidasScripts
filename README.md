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
    python2.7 setup.pyt install --prefix=$HOME/.local

This will install the python package into the ~/.local directory.

IMPORTANT: Inorder to have these packages work properly on both titan01 and lxmpet
you must run the command once on titan01 (python2.6), and a second time on lxmpet
using python2.7.

# General Information

Each script is generally tied to one "button" on the MIDAS status page, and its
function can be derived from the name of the script. For example, the scirpt
"afgOnOff.py" toggles the state of the quadrupole AFG, while the scirpt
"afgDipoleOnOff.py" toggles the state of the swift/dipole AFG.
