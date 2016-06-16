#!/bin/bash

# Convert the file on run stop
sh /home/mpet/local/scripts/convertOnRunStop.sh

### This is for the "old" PerlRC script.
### Kept for historical purposes at the moment.
### This will be deleted in the future.
#sleep 1
# Run python run control script
# Use the "old" PerlRC scripts:
#sh /home/mpet/vr/perl/PerlRC/perlrc.sh

# Use the "new" pythonrc scripts:
# Ensure we run on titan01, since the python versions are different
ssh mpet@titan01 "python /home/mpet/local/scripts/pythonrc.py"
