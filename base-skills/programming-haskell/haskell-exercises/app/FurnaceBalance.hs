module Main where

import System.Directory (createDirectoryIfMissing)
import Graphics.Rendering.Chart.Easy
import Graphics.Rendering.Chart.Backend.Cairo
import Physics.Furnace.Balance (OdeInputs(..), solveProblem, toCsv)

getSoln :: RealFloat a => [(a, [a])] -> Int -> a -> [(a, a)]
getSoln sol n xmult = [(t, xmult * x !! n) | (t, x) <- sol]

main :: IO ()
main = do
    -- Parse inputs
    -- fileContent <- readFile "ode-system-inputs.hs";
    -- let inputs = (read fileContent :: OdeInputs)

    createDirectoryIfMissing True "results"

    -- Create inputs.
    let inputs = OdeInputs {
        chamberVolume = 250.0,
        chamberPressure = 101425.0,
        chamberTemperature = 1073.15,
        renewalFlowRate = 4.0,
        pureSpeciesFlowRates = [0.145, 0.0, 0.0],
        renewalFlowComposition = [3.0e-05, 0.05, 0.0],
        surfaceRateConstants = [0.01, 10.0, 15.0],
        integrationTime = 4000.0,
        integrationStep = 15.0,
        initialComposition = [0.001, 0.05, 0.0001],
        saveResultsAs = "results/FurnaceBalance.csv"
        }

    -- Integrate problem.
    let solution = solveProblem inputs

    -- Dump results
    writeFile (saveResultsAs inputs) (toCsv solution ',')

    -- Plot results
    toFile def "results/FurnaceBalance.png" $ do
        layout_title .= "Simulation of composition dynamics"
        layout_background .= solidFillStyle (opaque white)
        layout_foreground .= (opaque black)
        layout_left_axis_visibility . axis_show_ticks .= False
        plot (line "x0 (x10)" [getSoln solution 0 1.0e+01])
        plot (line "x1 (x1)" [getSoln solution 1 1.0e+00])
        plot (line "x2 (x5)" [getSoln solution 2 5.0e+00])
