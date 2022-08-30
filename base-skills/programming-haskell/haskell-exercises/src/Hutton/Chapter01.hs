module Hutton.Chapter01 where

-- 3. Deﬁne a function product that produces the product of a list of numbers,
-- and show using your deﬁnition that product [2,3,4] “ 24 .
product' :: [Int] -> Int
product' [] = 1
product' (x:xs) = x * product' xs

-- 4. How should the deﬁnition of the function qsort be modiﬁed so that it pro-
-- duces a reverse sorted version of a list?
qsortrev :: Ord a => [a] -> [a]
qsortrev [] = []
qsortrev (x:xs) = qsortrev larger ++ [x] ++ qsortrev smaller
    where
        smaller = [a | a <- xs, a <= x]
        larger  = [b | b <- xs, b > x]

-- 5. What would be the eﬀect of replacing <= by < in the original deﬁnition of
-- qsort? Hint: consider the example qsort [2,2,3,1,1].
qsortmod :: Ord a => [a] -> [a]
qsortmod [] = []
qsortmod (x:xs) = qsortmod smaller ++ [x] ++ qsortmod larger
    where
        smaller = [a | a <- xs, a < x]
        larger = [b | b <- xs, b > x]
