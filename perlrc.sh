### Call pythonrc.py to perform PerlRC scans.
### The program will remain to be called PerlRC, even through it was re-written to use python,
### mainly for historical reasons.

ssh mpet@titan01 "python /home/mpet/local/scripts/pythonrc.py $*"

### These are the old commands. These will be removed in the furute.
#perl -I/home/mpet/local/perl /home/mpet/vr/perl/PerlRC/perlrc.pl $*
#ssh mpet@titan01 "python /home/mpet/Aaron/TitanMidasScripts/pythonmidas/pythonrc.py $*"
