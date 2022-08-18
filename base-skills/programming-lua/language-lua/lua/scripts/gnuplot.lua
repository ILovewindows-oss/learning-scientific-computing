-- Import required modules.
local extensions = require("extensions")

-- Declare current module object.
local gnuplot = {}

-- Keep a global instance of gnuplot active.
local gnuplotPipe

-- Data block counter.
local blockName = 0

------------------------------------------------------------------------------ 
-- BASE FUNCTIONS
------------------------------------------------------------------------------ 

-- data = {{x, y}, ...}
local function writeInlineData(file, data)
    -- Increment blockName and set header to table.
    blockName = blockName + 1
    file:write("$BLOCK" .. blockName  .. " << EOD\n")
    file:write("KEYS: X Y\n")

    -- Add data entries in block.
    for _, record in ipairs(data) do
        file:write("   " .. tostring(record[1]))
        local recordLength = #record
        for i = 2, recordLength do
            file:write(" " .. tostring(record[i]))
        end
        file:write("\n")
    end

    -- Close current block.
    file:write('EOD\n\n')
end
 
-- Run table of gnuplot commands in a row.
function gnuplot.execute(commands)
    -- Reset block counter and increment in loop.
    blockName = 0

    -- Make sure a connection to gnuplot is available.
    gnuplotPipe = gnuplotPipe or io.popen("gnuplot", "w")

    -- Initialize data blocks.
    dataBlocks = {}

    -- Initialize plot blocks.
    plotBlocks = {}

    -- Run general commands and accumulate blocks.
    for _, command in ipairs(commands) do
        if type(command) == "string" then
            if not extensions.startswith(command, "$BLOCK") then
                gnuplotPipe:write(command .. "\n")
            else
                table.insert(plotBlocks, command)
            end
        elseif type(command) == "table" then
            table.insert(dataBlocks, command)            
        end
    end

    -- Run data blocks.
    for _, command in ipairs(dataBlocks) do
        writeInlineData(gnuplotPipe, command)
    end

    -- Run plot commands.
    gnuplotPipe:write("plot ")
    for _, command in ipairs(plotBlocks) do
        gnuplotPipe:write(command)

        if #plotBlocks > 1 then
            gnuplotPipe:write(", ")
        end
    end

    gnuplotPipe:flush()
end

------------------------------------------------------------------------------ 
-- NEW API
------------------------------------------------------------------------------ 

function gnuplot.startPlot(outputFileName, width, height)
    -- Reset on starting new plot.
    blockName = 0

    -- Default starting lines with pngcairo
    return {
        "set terminal pngcairo enhanced fontscale 0.7 size "
            .. (width or 600) .. "," .. (height or 500),
        "set output '" .. outputFileName .. "'"
    }
end

function gnuplot.setTitle(plot, title)
    table.insert(plot, "set title '" .. title .. "' font 'Arial,20'")
end

function gnuplot.setXLabel(plot, xlabel)
    table.insert(plot, "set xlabel '" .. xlabel .. "' font 'Arial,16'")
end

function gnuplot.setYLabel(plot, ylabel)
    table.insert(plot, "set ylabel '" .. ylabel .. "' font 'Arial,16'")
end

function gnuplot.setLabels(plot, xlabel, ylabel)
    gnuplot.setXLabel(plot, xlabel)
    gnuplot.setYLabel(plot, ylabel)
end

function gnuplot.setKey(plot, position)
    position = position or "top right"
    table.insert(plot, "set key " .. position .. " font 'Arial,12'")
end

function gnuplot.setGrid(plot, active)
    if not active then
        return
    end

    table.insert(plot, "set style line 999 lc rgb '#808080' lt 0 lw 1")
    table.insert(plot, "set grid back ls 999")
end

function gnuplot.setStyleLine(plot, no, linetype, color, weight, point)
    table.insert(plot, "set style line " .. no .. " lt " .. linetype ..
                        " lc rgb '" .. color .. "' lw " .. weight ..
                        " pt " .. point)
end

function gnuplot.plotLines(plot, data, label, ls)
    -- Increment block counter to later access.
    blockName = blockName + 1
    table.insert(plot, data)
    table.insert(plot, "$BLOCK" .. blockName .. " using 1:2 with lines "
                 .. "ls " .. ls .. " title '" .. label .. "'")
end

return gnuplot
