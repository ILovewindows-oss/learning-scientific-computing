module Hutton.Spec.Chapter07 where

-- import Control.Exception (evaluate)
import Test.Hspec (Spec, describe, it, shouldBe, shouldSatisfy)
import Hutton.Chapter07 (
    applyfp,
    all',
    any',
    takeWhile',
    dropWhile',
    map',
    filter',
    dec2int,
    chop8,
    map'',
    altMap,
    luhn
    )
import Hutton.Extended.Chapter07.TransmitExercise (
    transmitPass,
    transmitFail
    )

specsChapter07 :: Spec
specsChapter07 = describe "Chapter 07" $ do
    it "applyfp" $
        shouldBe (applyfp (*2) (>5) [1..10]) [12,14,16,18,20]
    it "all'" $
        shouldBe (all' (>2) [1..5]) False
    it "any'" $
        shouldBe (any' (>2) [1..5]) True
    it "takeWhile'" $
        shouldBe (takeWhile' (<3) [1..5]) [1,2]
    it "dropWhile'" $
        shouldBe (dropWhile' (<3) [1..5]) [3,4,5]
    it "map'" $
        shouldBe (map' (*2) [1..3]) [2,4,6]
    it "filter'" $
        shouldBe (filter' (<3) [1..3]) [1,2]
    it "dec2int" $
        shouldBe (dec2int [2,3,4,5]) 2345
    it "chop8" $
        shouldBe (chop8 [1..10]) [[1..8],[9,10]]
    it "map''" $
        shouldBe (map'' (*(2 :: Int)) [1..3]) [2,4,6]
    it "transmitPass" $
        shouldBe (transmitPass "Hey!") "Hey!"
    it "transmitFail" $
        shouldSatisfy ((transmitFail "Hey!")) (not . null)
        -- FIXME why can't I get the proper error!?
        -- shouldThrow (evaluate (transmitFail "Hey!"))
        --             (errorCall "Non-Parity faulty transmission")
    it "altMap" $
        shouldBe (altMap (+10) (+100) ([0,1,2,3,4] :: [Int])) [10,101,12,103,14]
    it "luhn" $
        shouldBe (luhn [1,7,8,4]) True
    it "luhn" $
        shouldBe (luhn [4,7,8,3]) False