module Numerical.Integrator (euler) where

import Typing (Nb, Triple)

-- Basic Euler integrator (to be replaced by RK4).
euler :: (Triple -> (Nb, Nb)) -> Triple -> Nb -> Nb -> [Triple]
euler f (y0, t0, tk0) dy yf = triples
    where iterator = iterate $ eulerStep f dy
          triples  = takeWhile (\(y, t, tk) -> y <= yf) $ iterator (y0, t0, tk0)
          eulerStep f dy (y, t, tk) = (ynew, tnew, tknew)
              where ynew  = y + dy
                    tnew  = t + dy * dt
                    tknew = tk + dy * dtk
                    (dtk, dt) = f (y, t, tk)
