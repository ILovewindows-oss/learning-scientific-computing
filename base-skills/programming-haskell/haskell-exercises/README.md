# Programming in Haskell

Learning Haskell with Hutton's [Programming in Haskell](https://www.cs.nott.ac.uk/~pszgmh/pih.html).

Please consider doing your own exercises, only look up here if really stuck on a solution.

There is no warranty what I have done is correct (other then the tests), I am also learning Haskell.

## Build

**NOTE:** if compiling on Windows it is failing because of `cairo` dependency on `pkg-config>=0.9.0`. After trying some tweaks on mingw I dropped Windows support.

To install locally the proper version of GHC run `stack setup`.

Once that is finished, build project with `stack build`.

Now run tests `stack test`.
