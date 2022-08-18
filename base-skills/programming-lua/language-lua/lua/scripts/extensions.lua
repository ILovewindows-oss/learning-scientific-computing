
-- Declare current module object.
local extensions = {}

-- Helper method for getting string start match.
function extensions.startswith(String, Start)
    return string.sub(String, 1, string.len(Start)) == Start
end

-- Get environment variable.
function extensions.getfenv(fn)
    local i = 1
    while true do
        local name, val = debug.getupvalue(fn, i)
        if name == "_ENV" then
            return val
        elseif not name then
            break
        end
        i = i + 1
    end
end

-- Set environment variable.
function extensions.setfenv(fn, env)
    local i = 1
    while true do
        local name = debug.getupvalue(fn, i)
        if name == "_ENV" then
            callback = function() return env end
            debug.upvaluejoin(fn, i, (callback), 1)
            break
        elseif not name then
            break
        end
        i = i + 1
    end

    return fn
end

return extensions
