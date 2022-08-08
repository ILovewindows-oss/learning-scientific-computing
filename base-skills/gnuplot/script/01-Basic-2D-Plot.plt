# 
# Basic 2D Plot
# 

set terminal pngcairo size 600,600 enhanced font "Verdana,10"

set size square 1.0,1.0
set output "01-Basic-2D-Plot.png"
set decimalsign "."

set title "Some random data"
set xlabel "Coordinate [a.u.]"
set ylabel "Measurement [a.u.]"

set xrange [-0.2:5.2]
set yrange [-1.5:2.0]

set format x "{%.1f}"
set format y "{%.1f}"

set style line 100 lc rgb "#000000" dashtype 0
set style line 200 lc rgb "#FF0000" dashtype 1 pt 5

set grid linestyle 100
set key spacing 2.0 box opaque

DATA = "../data/points2d.dat"

plot DATA using 1:2:3 ls 200 with yerrorbars title "Values",\
     DATA using 1:2 ls 200 smooth csplines title ""
