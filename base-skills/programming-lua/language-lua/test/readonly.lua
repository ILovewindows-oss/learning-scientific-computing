-- make global variables readonly
-- NOTE: this assumes running from root with the following command
-- dist\bin\lua test\readonly.lua
package.path = package.path .. ';lua/scripts/?.lua'

local extensions = require("extensions")

local f = function (t,i) error("cannot redefine global variable `"..i.."'",2) end
local g = {}
local G = extensions.getfenv(f)

setmetatable(g, {__index=G, __newindex=f})
extensions.setfenv(f, g)

-- an example
rawset(g, "x", 3)
x = 2
y = 1	-- cannot redefine `y'
print(y)