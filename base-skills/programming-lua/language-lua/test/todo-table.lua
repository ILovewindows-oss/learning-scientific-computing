-- make table, grouping all data for the same item
-- input is 2 columns (item, data)

local A

while 1 do
 local l = io.read()
 if l == nil then break end

 local _, _, a, b = string.find(l, '"?([_%w]+)"?%s*(.*)$')
 
 if a ~= A and a ~= nil then 
    A = a io.write("\n",a,":")
 end
 if b ~= nil then 
    io.write(" ", b)
 end
end

io.write("\n")
