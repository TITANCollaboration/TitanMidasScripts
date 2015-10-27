import fnmatch
import time
import datetime
#import os
#import os.path
import subprocess


class extractFromPerlRCLog:
    logfile = '/titan/data1/mpet/PerlRC.log'
    #sdapath = '/home/mpet/sette/simplified1Danalysis/'
    sdapath = '/home/mpet/local/scripts/SDA/'
    datapath = '/titan/data1/mpet/'
    s1dafile = sdapath + 'simplifiedScan1Danalysis_input_AG.dat'

    def __init__(self):
        with open(self.logfile) as f:
            self.lines = f.readlines()
            f.close()
        with open(self.s1dafile) as f:
            self.s1da = f.readlines()
            f.close()

    def get_last_scan(self):
        filtered = fnmatch.filter(self.lines, '=== NEW PerlRC scan at*')
        i = 0
        while True:
            i += 1
            if self.lines[-i] == filtered[-1]:
                break
        self.lastScan = self.lines[-i:]

    def last_scan_runs(self):
        self.filesToConvert = []
        for l in self.lastScan:
            if l[0] == "<":
                self.filesToConvert.append(l)

    def last_scan_filenames(self):
        self.runFilenames = ['run' + f.replace('#', ' ').replace('>', ' ')
                             .split()[1].zfill(5) + '.mid'
                             for f in self.filesToConvert]

    def last_scan_values(self):
        self.runValues = [f.replace('=', ';').split(';')[1]
                          for f in self.filesToConvert]
        return self.runValues

    def last_scan_variable(self):
        self.runVariable = [f[f.find('>') + 2:f.find('=')]
                            for f in self.filesToConvert]
        if self.runVariable.count(self.runVariable[0]) \
           == len(self.runVariable):
            self.runVariable = self.runVariable[0]
        return self.runVariable

    def get_mca_range(self):
        self.mca = '0 200'
        if self.s1da[4].strip() == 'MCA Range:':
            self.mca = self.s1da[5].strip()
        return self.mca

    def get_plot_individual(self):
        self.plot_individual = 0
        if self.s1da[6].strip() == 'Plot Indiviudal?':
            temp = self.s1da[7].strip()
            if temp == 'n':
                self.plot_individual = 0
            else:
                self.plot_individual = 1
        return self.plot_individual

    def get_plot_position(self):
        self.plot_position = 0
        if self.s1da[8].strip() == 'Plot Positions?':
            temp = self.s1da[9].strip()
            if temp == 'n':
                self.plot_position = 0
            else:
                self.plot_position = 1
        return self.plot_position

    def last_scan_date(self):
        l = self.lastScan[0]
        dateLine = l.split(' ')
        s = dateLine[7] + " " + dateLine[8] + " " + dateLine[9]
        t = time.strptime(s, "%b %d, %Y")[0:3]
        dateStart = datetime.date(t[0], t[1], t[2])
        self.date = dateStart.strftime("%Y%m%d")
        return self.date

    def last_scan_type(self):
        l = self.lastScan[1]
        l = l.replace('\"', ' ').split()
        return l[4]

    def output_header(self):
        oldheader = self.s1da[0:11]
        restoffile = self.s1da[11:]
        #print oldheader
        #print restoffile[0]

        l = oldheader[3].strip()
        l = l[:-9]
        l = l + self.last_scan_date() + "/" + "\n"
        #print l
        oldheader[3] = l

        with open(self.s1dafile, 'w+') as f:
            for l in oldheader:
                f.write(l)
            for l in self.filesToConvert:
                f.write(l)
            f.write("end\n\n")
            for l in restoffile:
                f.write(l)
            f.close()

    def run_scripts(self):
        p = subprocess.Popen(self.sdapath + 'simplifiedScan1Danalysis_AG.sh',
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self.sdapath, shell=True)
        print p.communicate()[0]

    def convert_file(self, filename):
        #p = subprocess.Popen('/home/mpet/sette/simplified1Danalysis/m2e_se.sh ' + self.datapath + self.last_scan_date() + '/' + filename,
        #                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                     cwd='/home/mpet/sette/simplified1Danalysis/', shell=True)
        p = subprocess.Popen(self.sdapath + 'm2e_se.sh ' + self.datapath +
                             self.last_scan_date() + '/' + filename,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             cwd=self.sdapath,
                             shell=True)
        print p.communicate()

    def convert_files(self):
        for f in self.runFilenames:
            self.convert_file(f)

    def write_plot_TOF_file(self):
        with open(self.sdapath + 'fileListPlotTOF.dat', 'w') as f:
            f.write(self.get_mca_range() + '\n')
            f.write(self.sdapath + 'data/' + '\n')
            f.write(str(self.get_plot_individual()) + '\n')
            f.write(str(self.last_scan_variable()) + '\n')

            self.last_scan_filenames()
            self.last_scan_values()
            for i in xrange(len(self.runFilenames)):
                l = self.runFilenames[i]
                m = self.runValues[i]
                f.write(l[:-4] + '_se_test.dat' + ' ' + m + '\n')

    def convert_PerlRC(self):
        self.get_last_scan()
        self.last_scan_runs()
        self.write_plot_TOF_file()
        self.convert_files()
        self.output_header()
