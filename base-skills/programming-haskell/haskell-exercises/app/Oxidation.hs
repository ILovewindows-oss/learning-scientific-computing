module Main where

import System.Environment (getArgs)
import Physics.Oxidation.Model (modelSolver)

main :: IO ()
main = do
  args <- getArgs
  case args of
    [t, tk, tw, l, h, tc, tm, yf, dy] -> modelSolver (read t) (read tk)
        (read tw) (read l) (read h) (read tc) (read tm) (read yf) (read dy)
    _ -> putStrLn "Usage: Oxidation t tk tw l h tc tm yf dy"
