#!/bin/bash

# 2015.10.13 ATG
# The old ODB command was: /home/mpet/mb/perlrcmb.sh &
# This file was created to help centralize all of the MIDAS scripts

# Convert the file on run stop
sh /home/mpet/Aaron/TitanMidasScripts/convertOnRunStop.sh

# Run python run control script
# Use the "old" PerlRC scripts:
#sh /home/mpet/vr/perl/PerlRC/perlrc.sh
# Use the "new" pythonrc scripts:
# Ensure we run on titan01, since the python versions are different
ssh mpet@titan01 "python /home/mpet/local/scripts/pythonrc.py"
