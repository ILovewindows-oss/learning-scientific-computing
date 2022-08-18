package.path = package.path .. ';../lua/scripts/?.lua'

local gnuplot = require("gnuplot")
local csv = require("csv")

local data = {}
local f = csv.open("sample-titanic.csv", { header = true })

for fields in f:lines() do
    fare = math.tointeger(fields["Fare"]) or 1

    if fare <= 0  then
        print(fare)
    end
--     for i, v in ipairs(fields) do
--         print(i, v) 
--     end
end

print('second')
for fields in f:lines() do
    fare = math.tointeger(fields["Fare"]) or 1

    if fare <= 0  then
        print(fare)
    end
--     for i, v in ipairs(fields) do
--         print(i, v) 
--     end
end