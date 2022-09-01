module Hutton.Spec.Chapter04 where

import Test.Hspec (Spec, describe, it, shouldBe)
import Hutton.Chapter04 (
    halve,
    third',
    third'',
    third''',
    safetail',
    safetail'',
    safetail''',
    mult,
    luhn
    )

specsChapter04 :: Spec
specsChapter04 = describe "Chapter 04" $ do
    it "halve" $
        shouldBe (halve [1,2,3,4,5,6]) ([1,2,3],[4,5,6])
    it "third'" $
        shouldBe (third' [1..10]) 3
    it "third''" $
        shouldBe (third'' [1..10]) 3
    it "third'''" $
        shouldBe (third''' [1..10]) 3
    it "safetail'" $
        shouldBe (safetail' [1..10]) [2..10]
    it "safetail''" $
        shouldBe (safetail'' [1..10]) [2..10]
    it "safetail'''" $
        shouldBe (safetail''' [1..10]) [2..10]
    it "mult" $
        shouldBe (((mult 1) 2) 3) 6
    it "luhn" $
        shouldBe (luhn 1 7 8 4) True
    it "luhn" $
        shouldBe (luhn 4 7 8 3) False
