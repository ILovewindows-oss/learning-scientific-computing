module Hutton.Extended.Chapter07.TransmitExercise where

import Data.Char

------------------------------------------------------------------------------
-- TRANSMIT
--
-- Binary string transmitter example from chapter 7 of Programming
-- in Haskell, Graham Hutton, Cambridge University Press, 2016.
------------------------------------------------------------------------------

-- Types

type Bit = Int
type Channel = ([Bit] -> [Bit])

-- Base conversion

bin2int :: [Bit] -> Int
bin2int = foldr (\xs x -> xs + 2*x) 0

int2bin :: Int -> [Bit]
int2bin 0 = []
int2bin n = mod n 2 : int2bin (div n 2)

make8 :: [Bit] -> [Bit]
make8 bits = take 8 (bits ++ repeat 0)

-- Parity functions

addParity :: [Bit] -> [Bit]
addParity bits | (even . sum) bits = bits ++ [0]
               | otherwise         = bits ++ [1]

isFidel :: [Bit] -> Bit -> Bool
isFidel bits 0 = not (isFidel bits 1)
isFidel bits 1 | (even . sum) bits = False
               | otherwise         = True
isFidel _ _    = error "Empty list of bits"

checkParity :: [Bit] -> [Bit]
checkParity bits | isFidel (init bits) (last bits) = init bits
                 | otherwise = error "Non-Parity faulty transmission"

-- Transmission

encode :: String -> [Bit]
encode = concat . map (addParity . make8 . int2bin . ord)

chop :: Int -> [Bit] -> [[Bit]]
chop _ []   = []
chop n bits = take n bits : chop n (drop n bits)

decode :: [Bit] -> String
decode bits = map (chr . bin2int . checkParity) (chop 9 bits)

-- Simulation

transmiter :: Channel -> (String -> String)
transmiter ch = decode . ch . encode

channelPass :: Channel
channelPass = id

channelFail :: Channel
channelFail xs = [swapbit x | (_, x) <- zip [0 :: Int, 8..] xs]
    where swapbit y = if y == 0 then 1 else 0

transmitPass :: String -> String
transmitPass = transmiter channelPass

transmitFail :: String -> String
transmitFail = transmiter channelFail
