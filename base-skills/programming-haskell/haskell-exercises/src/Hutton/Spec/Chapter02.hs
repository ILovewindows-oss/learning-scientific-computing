module Hutton.Spec.Chapter02 where

import Test.Hspec (Spec, describe, it, shouldBe)
import Hutton.Chapter02 (
    last',
    init',
    init''
    )

specsChapter02 :: Spec
specsChapter02 = describe "Chapter 02" $ do
    it "last'" $
        shouldBe (last' [2, 3, 4]) 4
    it "init'" $
        shouldBe (init' [2, 3, 4]) [2, 3]
    it "init''" $
        shouldBe (init'' [2, 3, 4]) [2, 3]
