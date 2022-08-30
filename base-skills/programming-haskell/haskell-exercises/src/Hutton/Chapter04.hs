module Hutton.Chapter04 where

-- 1. Using library functions, deﬁne a function halve :: [a] -> ([a],[a]) that
-- splits an even-lengthed list into two halves. For example:
-- > halve [1,2,3,4,5,6]   ---> ([1,2,3],[4,5,6])
halve :: [Int] -> ([Int], [Int])
halve xs = splitAt (div (length xs) 2) xs

-- 2. Deﬁne a function third :: [a] -> a that returns the third element in a list
-- that contains at least this many elements using:
--     a. head and tail;
--     b. list indexing !!;
--     c. pattern matching.
third' :: [Int] -> Int
third' a = head (tail (tail a))

third'' :: [Int] -> Int
third'' a = a !! 2

third''' :: [Int] -> Int
third''' []        = error "List must be at least 3-element long"
third''' (_:[])    = error "List must be at least 3-element long"
third''' (_:_:[])  = error "List must be at least 3-element long"
third''' (_:_:a:_) = a

-- 3. Consider a function safetail :: [a] -> [a] that behaves in the same way
-- as tail except that it maps the empty list to itself rather than producing an
-- error. Using tail and the function null :: [a] -> Bool that decides if a
-- list is empty or not, deﬁne safetail using:
--     a. a conditional expression;
--     b. guarded equations;
--     c. pattern matching.
safetail' :: [Int] -> [Int]
safetail' a = if null a then [] else tail a

safetail'' :: [Int] -> [Int]
safetail'' a | null a    = []
             | otherwise = tail a

safetail''' :: [Int] -> [Int]
safetail''' [] = []
safetail''' (_:xs) = xs

-- 7. Show how the meaning of the following curried function deﬁnition can be
-- formalised in terms of lambda expressions:
--   mult :: Int -> Int -> Int -> Int
--   mult x y z = x*y*z
mult :: (Int -> (Int -> (Int -> Int)))
mult = \x -> (\y -> (\z -> x * y * z))

-- 8. The Luhn algorithm is used to check bank card numbers for simple errors
-- such as mistyping a digit, and proceeds as follows:
--    + consider each digit as a separate number;
--    + moving left, double every other number from the second last;
--    + subtract 9 from each number that is now greater than 9;
--    + add all the resulting numbers together;
--    + if the total is divisible by 10, the card number is valid.
--
-- Deﬁne a function luhnDouble :: Int -> Int that doubles a digit and sub-
-- tracts 9 if the result is greater than 9. For example:
-- > luhnDouble 3   ---> 6
-- > luhnDouble 6   ---> 3
--
-- Using luhnDouble and the integer remainder function mod , deﬁne a function
-- luhn :: Int -> Int -> Int -> Int -> Bool that decides if a four-digit
-- bank card number is valid. For example:
-- > luhn 1 7 8 4   ---> True
-- > luhn 4 7 8 3   ---> False
--
-- In the exercises for chapter 7 we will consider a more general version of this
-- function that accepts card numbers of any length.
luhnDouble :: (Ord a, Num a) => a -> a
luhnDouble a | b < 10    = b
             | otherwise = b - 9
             where b = 2 * a

luhn :: Int -> Int -> Int -> Int -> Bool
luhn _ b c d = v
    where s = sum [luhnDouble b, luhnDouble c, luhnDouble d]
          v = mod s 10 == 0
