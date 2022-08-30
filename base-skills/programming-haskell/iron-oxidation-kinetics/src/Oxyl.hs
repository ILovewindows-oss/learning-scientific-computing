module Oxyl ( modelSolver ) where

import Typing (Nb, Triple)
import Model.OdeSystem (rhs)
import Numerical.Integrator (euler)

modelSolver :: Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> Nb -> IO ()
modelSolver t tk tw l h tc tm yf dy = do
    putStrLn "\n*** WELCOME TO OXYL ***"
    putStrLn ("Initial oxide thickness ....... [nm] " ++ show t)
    putStrLn ("Initial steel temperature ...... [K] " ++ show tk)
    putStrLn ("Furnace wall temperature ....... [K] " ++ show tw)
    putStrLn ("Steel strip thickness .......... [m] " ++ show l)
    putStrLn ("Convection coefficient ... [W/(m.K)] " ++ show h)
    putStrLn ("Oxydation half thickness ...... [nm] " ++ show tc)
    putStrLn ("Oxydation exponent ............. [-] " ++ show tm)
    putStrLn ("End integration time ........... [s] " ++ show yf)
    putStrLn ("Integration time step .......... [s] " ++ show dy)

    let ode (y, t0, tk0) = rhs t0 tk0 tw l h tc tm
    let sol = euler ode (0, t, tk) dy yf

    writeFile "results.csv" (toCsv sol ',')
    putStrLn "*** GOOD-BYE ***\n"  

-- Prepare results for dumping as CSV file.
toCsv :: Show a => [(a, a, a)] -> Char -> String
toCsv solution sep = (unlines . csvTab) solution
    where
        listToString   = unwords . map show
        newLine xs     = [if x == ' ' then sep else x | x<-xs]
        csvTab triples = [newLine $ listToString [x, y, z] | (x, y, z) <- triples]
