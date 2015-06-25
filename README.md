# qcplot
scripts to create snr skyplot from teqc output

written under linux (ubuntu)
necessary programs: teqc, python, sort, gnuplot

example of usage:

1. run teqc: teqc +qc -nav brdc1690.15n bute1690.15o

2. create the plots: qcplot bute1690 sn1 all skyplot.png recplot.png

or

1. run teqc: teqc +qc -nav brdc1690.15n bute1690.15o

2. convert its output with qcplot: python qcplot.py bute1690 sn1. > data.txt

3. sort its output in order to plot weak signals at first: sort -k3 -r data.txt > data2.txt

4. plot with gnuplot: gnuplot skyplot.plt. output is skyplot.png
