@echo off

REM Configure project build.
cmake -S lua/ -B build/ -ULUA_USE_READLINE

REM Run build from command line.
devenv /build Release build/lua.sln /project INSTALL

REM Run all tests.
REM dist\bin\lua test\bisect.lua
REM dist\bin\lua test\cf.lua
REM dist\bin\lua test\echo.lua
REM dist\bin\lua test\env.lua
REM dist\bin\lua test\factorial.lua
REM dist\bin\lua test\fib.lua
REM dist\bin\lua test\fibfor.lua
REM dist\bin\lua test\globals.lua
REM dist\bin\lua test\hello.lua
REM dist\bin\lua test\life.lua
REM dist\bin\lua test\luac.lua
REM dist\bin\lua test\printf.lua
REM dist\bin\lua test\readonly.lua
REM dist\bin\lua test\sieve.lua
REM dist\bin\lua test\sort.lua
REM dist\bin\lua test\table.lua
REM dist\bin\lua test\trace-calls.lua
REM dist\bin\lua test\trace-globals.lua
REM dist\bin\lua test\xd.lua
