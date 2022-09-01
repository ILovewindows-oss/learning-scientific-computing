module Physics.Furnace.Balance where

-- Ideal gas constant [J/(mol.K)].
gasConstant :: Double
gasConstant = 8.31446261815324

-- TODO make compatible with Physics.Integrator.
-- Provides a simple forward Euler integration routine.
euler :: (RealFloat a) => ((a, [a]) -> [a]) -> (a, a, [a], a) -> [(a, [a])]
euler f (t0, tf, y0, dt) = xypairs
    where
        iterator = iterate $ eulerStep f dt
        xypairs = takeWhile (\(t, _) -> t <= tf) $ iterator (t0, y0)
        eulerStep f' dt' (t, y) = (tnew, ynew)
            where
                tnew = t + dt'
                ynew = [(y !! k) + dt' * (ydot !! k) | k <- [0..size]]
                ydot = f' (t, y)
                size = length y + (-1)

-- Heaviside step function.
heaviside :: (RealFloat a) => a -> a
heaviside u 
    | u < 0.0   = 0.0
    | u == 0.0  = 0.5
    | otherwise = 1.0

-- Implements a generic mass balance for the vector of species in the
-- furnace reactor. Notice here that instead of a tuple this function
-- returns a list to allow ease of extension and integration to the
-- generic integration function. This function is not aimed at being
-- used directly, but a specialized version with the parameters in
-- the second tuple already defined.
-- 
-- TODO: add boiler equation.
-- TODO: make constants `k` functions of time.
odeSpecies :: (RealFloat a) => (a, [a]) -> (a, a, [a], [a], [a]) -> [a]
odeSpecies (_, x) (n, q, u, xs, k) = [xdot0, xdot1, xdot2]
    where
        -- Reduction, oxidation, and decarburization rates.
        rdot0  = (k !! 0) * (x !! 1)
        rdot1  = (k !! 1) * (x !! 0)
        rdot2  = (k !! 2) * (x !! 0)
        -- Generation rates on a species basis.
        n_gen0 = rdot0 - rdot1 - rdot2
        n_gen1 = (-1) * n_gen0
        n_gen2 = rdot2
        -- Total outlet flow rate.
        n_out  = q + (sum u) + n_gen2
        -- Inlet flow rate on a species basis.
        n_in0  = q * (xs !! 0) + (u !! 0)
        n_in1  = q * (xs !! 1) + (u !! 1)
        n_in2  = q * (xs !! 2) + (u !! 2)
        -- Outlet flow rate on a species basis.
        n_out0 = n_out * (x !! 0)
        n_out1 = n_out * (x !! 1)
        n_out2 = n_out * (x !! 2)
        -- Molar balance on a species basis.
        xdot0 = (n_in0 - n_out0 + n_gen0) / n
        xdot1 = (n_in1 - n_out1 + n_gen1) / n
        xdot2 = (n_in2 - n_out2 + n_gen2) / n

-- Convert a list of ODE integration results to a CSV string. This
-- function assumes integration was done with `euler` or another
-- similar interface returning tuples of time-points and arrays of
-- values of integration variables.
toCsv :: Show a => [(a, [a])] -> Char -> String
toCsv solution sep = (unlines . csvTab) solution
    where
        listToString  = unwords . map show
        newLine xs    = [if x == ' ' then sep else x | x<-xs]
        csvTab tytab  = [newLine $ listToString $ t:y | (t, y) <- tytab]

-- Number of moles in ideal gas at given conditions.
molesInSystem :: Double -> Double -> Double -> Double
molesInSystem p v t = p * v / (gasConstant * t)

-- Parameters required by model
data OdeInputs = OdeInputs {
        chamberVolume :: Double,
        chamberPressure :: Double,
        chamberTemperature :: Double,
        renewalFlowRate :: Double,
        pureSpeciesFlowRates :: [Double],
        renewalFlowComposition :: [Double],
        surfaceRateConstants :: [Double],
        integrationTime :: Double,
        integrationStep :: Double,
        initialComposition :: [Double],
        saveResultsAs :: String
    }
    deriving (Show, Read)

getOde :: OdeInputs -> (Double, [Double]) -> [Double]
getOde inputs = \(t, x) -> odeSpecies (t, x)
                                      ((molesInSystem
                                        (chamberPressure inputs)
                                        (chamberVolume inputs)
                                        (chamberTemperature inputs)),
                                       (renewalFlowRate inputs),
                                       (pureSpeciesFlowRates inputs),
                                       (renewalFlowComposition inputs),
                                       (surfaceRateConstants inputs))

solveProblem :: OdeInputs -> [(Double, [Double])]
solveProblem inputs = euler (getOde inputs) 
                            (0.0, 
                             (integrationTime inputs),
                             (initialComposition inputs),
                             (integrationStep inputs))

-- If missing generate an inputs file with the following:
-- OdeInputs {
--         chamberVolume = 250.0,
--         chamberPressure = 101425.0,
--         chamberTemperature = 1173.15,
--         renewalFlowRate = 4.0,
--         pureSpeciesFlowRates = [0.145, 0.0, 0.0],
--         renewalFlowComposition [3.0e-05, 0.05, 0.0],
--         surfaceRateConstants = [0.01, 10., 15.0],
--         integrationTime = 1200.0,
--         integrationStep = 15.0,
--         initialComposition = [0.001, 0.05, 0.0001],
--         saveResultsAs = "ode-system.csv"
--         }
