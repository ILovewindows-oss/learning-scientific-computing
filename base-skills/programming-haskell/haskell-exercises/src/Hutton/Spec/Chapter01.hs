module Hutton.Spec.Chapter01 where

import Data.List (sort)
import Test.Hspec (Spec, describe, it, shouldBe)
import Hutton.Chapter01 (
    product',
    qsortrev,
    qsortmod
    )

specsChapter01 :: Spec
specsChapter01 = describe "Chapter 01" $ do
    it "product" $
        shouldBe (product' [2, 3, 4]) 24
    it "qsortrev" $
        shouldBe (qsortrev sampleList) (reverse $ sort sampleList)
    it "qsortmot" $
        shouldBe (qsortmod sampleList) [1, 2, 3]

sampleList :: [Int]
sampleList = [2, 2, 3, 1, 1]
