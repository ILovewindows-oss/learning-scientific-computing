-- read environment variables as if they were global variables
-- NOTE: this assumes running from root with the following command
-- dist\bin\lua test\env.lua
package.path = package.path .. ';lua/scripts/?.lua'

local extensions = require("extensions")

local f = function (t,i) return os.getenv(i) end

setmetatable(extensions.getfenv(f), {__index=f})

-- an example
print(a,USER,PATH)
