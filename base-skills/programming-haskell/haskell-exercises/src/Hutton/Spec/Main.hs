module Hutton.Spec.Main where

import Test.Hspec.Runner (hspec)
import Hutton.Spec.Chapter01 (specsChapter01)
import Hutton.Spec.Chapter02 (specsChapter02)
import Hutton.Spec.Chapter03 (specsChapter03)
import Hutton.Spec.Chapter04 (specsChapter04)
import Hutton.Spec.Chapter05 (specsChapter05)
import Hutton.Spec.Chapter06 (specsChapter06)
import Hutton.Spec.Chapter07 (specsChapter07)
import Hutton.Spec.Chapter08 (specsChapter08)
import Hutton.Spec.Chapter09 (specsChapter09)
import Hutton.Spec.Chapter10 (specsChapter10)
import Hutton.Spec.Chapter11 (specsChapter11)
import Hutton.Spec.Chapter12 (specsChapter12)
import Hutton.Spec.Chapter13 (specsChapter13)
import Hutton.Spec.Chapter14 (specsChapter14)
import Hutton.Spec.Chapter15 (specsChapter15)
import Hutton.Spec.Chapter16 (specsChapter16)
import Hutton.Spec.Chapter17 (specsChapter17)

mainHuttonSpec :: IO ()
mainHuttonSpec = hspec $ do
    specsChapter01
    specsChapter02
    specsChapter03
    specsChapter04
    specsChapter05
    specsChapter06
    specsChapter07
    specsChapter08
    specsChapter09
    specsChapter10
    specsChapter11
    specsChapter12
    specsChapter13
    specsChapter14
    specsChapter15
    specsChapter16
    specsChapter17
