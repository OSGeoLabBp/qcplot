#script to draw snr skyplot from qcplot.py output
#usage example:
#python qcplot bute1690 snr1
#sort -k3 -r data.txt > data2.txt
#gnuplot skyplot.plt 
set terminal png small size 480,360
set output 'skyplot.png'
set xrange [0:360]
set yrange [0:90]
set grid
set xlabel "Azimuth"
set ylabel "Elevation"
set xtics 30
set ytics 10
set palette defined (10 "red", 30 "yellow", 60 "dark-green")
set cbrange [10:60]
set title 'station: bute, date: 169/2015, type: snr1'
set label 1 'created by qcplot' at graph 0.9,-0.1 front
set label 2 'SNR [dB-Hz]' at graph 0.95,1.05 front
plot 'data2.txt' using 1:2:3 notitle palette pt 7 ps 0.5

