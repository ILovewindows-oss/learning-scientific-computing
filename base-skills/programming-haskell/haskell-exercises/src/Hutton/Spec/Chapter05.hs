module Hutton.Spec.Chapter05 where

import Test.Hspec (Spec, describe, it, shouldBe)
import Hutton.Chapter05 (
    sumSq,
    grid,
    square,
    replicate',
    pyths,
    perfects,
    nestedlc,
    positions,
    scalarproduct
    )

specsChapter05 :: Spec
specsChapter05 = describe "Chapter 05" $ do
    it "sumSq" $
        shouldBe (sumSq 1 100) 338350
    it "grid" $
        shouldBe (grid 1 2) [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]
    it "square" $
        shouldBe (square 2) [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
    it "replicate" $
        shouldBe (replicate' 3 True) [True,True,True]
    it "pyths" $
        shouldBe (pyths 10) [(3,4,5),(4,3,5),(6,8,10),(8,6,10)]
    it "perfects" $
        shouldBe (perfects 500) [6,28,496]
    it "nestedlc" $
        shouldBe (nestedlc [1,2] [3,4]) [(1,3), (1,4), (2,3), (2,4)]
    it "positions" $
        shouldBe (positions 3 [3, 1, 2, 3]) [0, 3]
    it "scalarproduct" $
        shouldBe (scalarproduct [1,2,3] [4,5,6]) 32
