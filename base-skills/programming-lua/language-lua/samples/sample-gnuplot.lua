package.path = package.path .. ';../lua/scripts/?.lua'

gnuplot = require("gnuplot")

local data1 = { {1, 1}, {2, 1}, {3, 2}, {4, 3}, {5, 5}, {6, 8} }
local data2 = { {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}, {6, 7} }

plot = gnuplot.startPlot("sample-gnuplot.png")

gnuplot.setTitle(plot, "Plot title")
gnuplot.setLabels(plot, "x-axis", "y-axis")

gnuplot.setKey(plot, "top left")
gnuplot.setGrid(plot, true)

gnuplot.setStyleLine(plot, 1, 1, "#000000", 2, 10)
gnuplot.plotLines(plot, data1, "line 1", 1)

gnuplot.setStyleLine(plot, 2, 1, "#FF0000", 2, 10)
gnuplot.plotLines(plot, data2, "line 2", 2)

gnuplot.execute(plot)