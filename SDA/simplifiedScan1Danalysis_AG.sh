#!/bin/bash
#
gcc -o s1da_makeInputFiles_AG s1da_makeInputFiles_AG.c -lm
./s1da_makeInputFiles_AG
./m2eseries_se.sh
#ssh titan01 ./sette/simplified1Danalysis/m2eseries_se.sh
