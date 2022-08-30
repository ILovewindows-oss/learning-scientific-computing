module Main where

import System.IO
import Hutton.Extended.Chapter09.CountdownInteractive

main :: IO ()
main =  do hSetBuffering stdout NoBuffering
           putStrLn "\nCOUNTDOWN NUMBERS GAME SOLVER"
           putStrLn "-----------------------------\n"
           putStr "Enter the given numbers : "
           ns <- readLn
           putStr "Enter the target number : "
           n  <- readLn
           display (solutions'' ns n)
