module Hutton.Spec.Chapter06 where

import Test.Hspec (Spec, describe, it, shouldBe)
import Hutton.Chapter06 (
    factorial,
    sumdown,
    (^%),
    euclid,
    and',
    concat',
    replicate',
    (!!%),
    elem',
    merge,
    msort,
    sum',
    take',
    last'
    )

specsChapter06 :: Spec
specsChapter06 = describe "Chapter 06" $ do
    it "factorial" $
        shouldBe (factorial (-2)) 2
    it "factorial" $
        shouldBe (factorial 3) 6
    it "sumdown" $
        shouldBe (sumdown 3) 6
    it "(^%)" $
        shouldBe (2 ^% 3) 8
    it "euclid" $
        shouldBe (euclid 6 27) 3
    it "and'" $
        shouldBe (and' [True,False]) False
    it "and'" $
        shouldBe (and' [True,True]) True
    it "concat'" $
        shouldBe (concat' [[1],[2]]) [1,2]
    it "replicate'" $
        shouldBe (replicate' 2 2) [2,2]
    it "(!!%)" $
        shouldBe ([1,2,3] !!% 2) 3
    it "elem'" $
        shouldBe (elem' 2 [1..3]) True
    it "elem'" $
        shouldBe (elem' 5 [1..3]) False
    it "merge" $
        shouldBe (merge [2,5,6] [1,3,4]) [1,2,3,4,5,6]
    it "msort" $
        shouldBe (msort [6,1,4,3]) [1,3,4,6]
    it "sum'" $
        shouldBe (sum' [1..3]) 6
    it "take'" $
        shouldBe (take' 3 [1..9]) [1,2,3]
    it "last'" $
        shouldBe (last' [1..9]) 9
