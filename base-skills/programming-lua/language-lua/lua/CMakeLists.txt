# -----------------------------------------------------------------------------
# CMakeLists.txt for lua.
# Here are provided the specific configurations for building the library.
# -----------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.12.3)

project ("lua" VERSION 5.4.3 DESCRIPTION "Lua Programming Language")

set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Configuration types" FORCE)
set(CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "Configuration types" FORCE)

# -----------------------------------------------------------------------------
# Set install path to package.
# -----------------------------------------------------------------------------

set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/../dist"
    CACHE STRING "Install directory" FORCE)

# -----------------------------------------------------------------------------
# General compilation definitions.
# -----------------------------------------------------------------------------

add_compile_definitions(LUA_COMPAT_5_3)

if (!MSVC)
    add_compile_definitions(LUA_USE_READLINE)
endif()

# -----------------------------------------------------------------------------
# Sources for library.
# -----------------------------------------------------------------------------

add_library(liblua STATIC
    src/lapi.c
    src/lapi.h
    src/lauxlib.c
    src/lauxlib.h
    src/lbaselib.c
    src/lcode.c
    src/lcode.h
    src/lcorolib.c
    src/lctype.c
    src/lctype.h
    src/ldblib.c
    src/ldebug.c
    src/ldebug.h
    src/ldo.c
    src/ldo.h
    src/ldump.c
    src/lfunc.c
    src/lfunc.h
    src/lgc.c
    src/lgc.h
    src/linit.c
    src/liolib.c
    src/ljumptab.h
    src/llex.c
    src/llex.h
    src/llimits.h
    src/lmathlib.c
    src/lmem.c
    src/lmem.h
    src/loadlib.c
    src/lobject.c
    src/lobject.h
    src/lopcodes.c
    src/lopcodes.h
    src/lopnames.h
    src/loslib.c
    src/lparser.c
    src/lparser.h
    src/lprefix.h
    src/lstate.c
    src/lstate.h
    src/lstring.c
    src/lstring.h
    src/lstrlib.c
    src/ltable.c
    src/ltable.h
    src/ltablib.c
    src/ltm.c
    src/ltm.h
    src/lua.c
    src/luac.c
    src/luaconf.h
    src/lua.h
    src/lua.hpp
    src/lualib.h
    src/lundump.c
    src/lundump.h
    src/lutf8lib.c
    src/lvm.c
    src/lvm.h
    src/lzio.c
    src/lzio.h
)

set_target_properties(liblua PROPERTIES PUBLIC_HEADER
    "src/lua.h;src/luaconf.h;src/lualib.h;src/lauxlib.h;src/lua.hpp")
    
if (MSVC)
    install(TARGETS liblua
            ARCHIVE DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
            PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_PREFIX}/include")
else()
    target_link_libraries(liblua m dl readline)
    install(TARGETS liblua
            LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/lib"
            PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_PREFIX}/include")
endif()

# -----------------------------------------------------------------------------
# Sources for interpreter.
# -----------------------------------------------------------------------------

add_executable(lua src/lua.c)

if (MSVC)
    set_property(TARGET lua APPEND PROPERTY LINK_LIBRARIES "$<$<CONFIG:Release>:liblua>")
    install(TARGETS lua RUNTIME DESTINATION "${CMAKE_INSTALL_PREFIX}/bin")
else()
    add_compile_definitions(LUA_USE_LINUX)
    set_property(TARGET lua APPEND PROPERTY LINK_LIBRARIES "$<$<CONFIG:Release>:liblua>")
    install(TARGETS lua LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/bin")
endif()

# -----------------------------------------------------------------------------
# Sources for compiler.
# -----------------------------------------------------------------------------

add_executable(luac src/luac.c)

if (MSVC)
    set_property(TARGET luac APPEND PROPERTY LINK_LIBRARIES "$<$<CONFIG:Release>:liblua>")
    install(TARGETS luac RUNTIME DESTINATION "${CMAKE_INSTALL_PREFIX}/bin")
else()
    add_compile_definitions(LUA_USE_LINUX)
    set_property(TARGET luac APPEND PROPERTY LINK_LIBRARIES "$<$<CONFIG:Release>:liblua>")
    install(TARGETS luac LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/bin")
endif()

# -----------------------------------------------------------------------------
# Manual pages.
# -----------------------------------------------------------------------------

install(FILES "doc/lua.1" DESTINATION "${CMAKE_INSTALL_PREFIX}/man/man1")
install(FILES "doc/luac.1" DESTINATION "${CMAKE_INSTALL_PREFIX}/man/man1")
