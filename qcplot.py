#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
.. module:: qcplot.py

.. moduleauthor:: Siki Zoltan, Takacs Bence

Sample application to plot teqc output
this python script merges teqc output files (.azi, .ele, .sn?)

usage of teqc: teqc +qc -nav brdc1690.15n bute1690.15o

the output of qcplot.py is sent to stdout which contains each measurement in a
separate line

format: azimuth elevation snr1 (or snr2)

example: python qcplot.py bute1690 sn1    

    :param argv[1]: file name
    :param argv[2]: type of plot sn1 (=snr1) or sn2 (=snr2)
"""

import sys

class qcfile(object):
    """ qcfile class handles a ...
    """

    def __init__(self, fname):
        """ constructor
        """
        self.fname = fname  # name of data file
        self.last = []     # last satelite list
        self.state = 0
        try:
            self.fp = open(fname, 'r')
        except IOError:
            self.fp = None
            self.state = -1
            return
        # skip first 3 lines
        buf = self.fp.readline().strip()
        if buf != "COMPACT2":
            self.fp.close()
            self.fp = None
            self.state = -2
            return
        self.fp.readline()
        self.fp.readline()

    def __del__(self):
        """ Destructor
        """
        if not self.fp is None:
            self.fp.close()

    def next(self):
        """ get next items from the next two lines of file

            :returns: a dictionary satelite id is the key
        """
        buf = self.fp.readline().strip()    #number and list of satellites
        if not buf:
            self.state = -3
            return None
        if buf != '-1': 
            self.last = buf.split()[1:]
        buf = self.fp.readline()    #azimuth/elevation/snr values of satellites
        if not buf:
            self.state = -3
            return None
        return dict(zip(self.last, buf.split()))
        
if len(sys.argv) < 3:
    print >> sys.stderr, "usage: ./qcplot.py filename plottype"
    exit(1)
if not (sys.argv[2] == 'sn1' or sys.argv[2] == 'sn2'):
    print >> sys.stderr, "usage: ./qcplot.py filename plottype"
    print >> sys.stderr, "plottype should be sn1 or sn2"
    exit(1)

ext = ('.azi', '.ele', '.' + sys.argv[2])
fn = sys.argv[1]
if fn[-4:] in ext:
    fn = fn[:-4]    # remove extension

[azi, ele, snr] = [qcfile(fn + x) for x in ext]
# check for error
for i in [azi, ele, snr]:
    if i.state != 0:
        print >> sys.stderr, "error with file: " + i.fname 
        exit(-1)

while 1:
    data_azi = azi.next()
    data_ele = ele.next()
    data_snr = snr.next()
    if azi.state != 0 or ele.state != 0 or snr.state != 0:
        break

    #output prn, azimuth, elevation, snr
    for prn in data_azi:
        if prn in data_snr:
            if float(data_azi[prn]) < 0:
                w = float(data_azi[prn]) + 360.0
            else:
                w = float(data_azi[prn])
            print("%.3f %s %s" % (w, data_ele[prn], data_snr[prn]))
