module Main where

import System.Environment (getArgs)
import Oxyl (modelSolver)

main :: IO ()
main = do
  args <- getArgs
  case args of
    [t, tk, tw, l, h, tc, tm, yf, dy] -> modelSolver (read t) (read tk)
        (read tw) (read l) (read h) (read tc) (read tm) (read yf) (read dy)
    _ -> putStrLn "Usage: oxyl-exe t tk tw l h tc tm yf dy"

-- stack run --allow-different-user -- 1e-12 300 1473 0.002 0 150e-09 3 100 0.1