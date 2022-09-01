module Hutton.Chapter07 where

-- 1. Show how the list comprehension [f x | x <- xs, p x] can be re-expressed
-- using the higher-order functions map and filter.
applyfp :: (Int -> Int) -> (Int -> Bool) -> [Int] -> [Int]
applyfp f p = map f . filter p

-- 2. Without looking at the deﬁnitions from the standard prelude, deﬁne the fol-
-- lowing higher-order library functions on lists.
-- a. Decide if all elements of a list satisfy a predicate:
-- all :: (a -> Bool) -> [Bool] -> Bool
all' :: (Int -> Bool) -> [Int] -> Bool
all' f xs = length xs == length (filter f xs)

-- b. Decide if any element of a list satisﬁes a predicate:
-- any :: (a -> Bool) -> [Bool] -> Bool
any' :: (Int -> Bool) -> [Int] -> Bool
any' f xs = length (filter f xs) > 0

-- c. Select elements from a list while they satisfy a predicate:
-- takeWhile :: (a -> Bool) -> [a] -> [a]
takeWhile' :: (Int -> Bool) -> [Int] -> [Int]
takeWhile' _ [] = []
takeWhile' f (x:xs)
  | f x       = x : takeWhile' f xs
  | otherwise = []

-- d. Remove elements from a list while they satisfy a predicate:
-- dropWhile :: (a -> Bool) -> [a] -> [a]
dropWhile' :: (Int -> Bool) -> [Int] -> [Int]
dropWhile' _ [] = []
dropWhile' f (x:xs)
  | f x       = dropWhile' f xs
  | otherwise = x : xs

-- 3. Redeﬁne the functions map f and filter p using foldr.
map' :: (Int -> Int) -> [Int] -> [Int]
map' f xs = foldr (\y ys -> (f y):ys) [] xs

filter' :: (Int -> Bool) -> [Int] -> [Int]
filter' f xs = foldr (sely) [] xs
    where sely y ys
            | f y == True = y:ys
            | otherwise   = ys

-- 4. Using foldl, deﬁne a function dec2int :: [Int] -> Int that converts a
-- decimal number into an integer. For example:
-- > dec2int [2,3,4,5]  ---> 2345
dec2int :: [Int] -> Int
dec2int = foldl (\a b -> 10 * a + b) 0

-- 5. Without looking at the deﬁnitions from the standard prelude, deﬁne the
-- higher-order library function curry that converts a function on pairs into
-- a curried function, and, conversely, the function uncurry that converts a
-- curried function with two arguments into a function on pairs.
-- Hint: ﬁrst write down the types of the two functions.
curry' :: ((a, b) -> c) -> a -> b -> c
curry' f = (\x y -> f (x, y))

uncurry' :: (a -> b -> c) -> (a, b) -> c
uncurry' f = (\(x, y) -> f x y)

-- 6. A higher-order function unfold that encapsulates a simple pattern of
-- recursion for producing a list can be deﬁned as follows:
-- > unfold p h t x | p x = []
-- >                | otherwise = h x : unfold p h t (t x)
-- That is, the function unfold p h t produces the empty list if the predicate
-- p is true of the argument value, and otherwise produces a non-empty list by
-- applying the function h to this value to give the head, and the function t
-- to generate another argument that is recursively processed in the same way
-- to produce the tail of the list. For example, the function int2bin can be
-- rewritten more compactly using unfold as follows:
-- > int2bin = unfold (== 0) (‘mod‘ 2) (‘div‘ 2)
-- Redeﬁne the functions chop8, map f and iterate f using unfold.
-- type Bit = Int

unfold :: (a -> Bool) -> (a -> b) -> (a -> a) -> a -> [b]
unfold p h t x | p x = []
               | otherwise = h x : unfold p h t (t x)

type Bit = Int

chop8 :: [Bit] -> [[Bit]]
chop8 = unfold (== []) (take 8) (drop 8)

map'' :: Eq a => (a -> b) -> [a] -> [b]
map'' f = unfold (== []) (f . head) (drop 1)

-- TODO how to test?
iterate' :: Eq a => (a -> a) -> a -> [a]
iterate' f x = unfold (const False) id f x

-- 7. Modify the binary string transmitter example to detect simple transmission
-- errors using the concept of parity bits. That is, each eight-bit binary number
-- produced during encoding is extended with a parity bit, set to one if the
-- number contains an odd number of ones, and to zero otherwise. In turn, each
-- resulting nine-bit binary number consumed during decoding is checked to
-- ensure that its parity bit is correct, with the parity bit being discarded if
-- this is the case, and a parity error being reported otherwise.
-- Hint: the library function error :: String -> a displays the given string
-- as an error message and terminates the program; the polymorphic result type
-- ensures that error can be used in any context.
-- Answer in Hutton.Extended.Chapter07.TransmitExercise

-- 8. Test your new string transmitter program from the previous exercise using a
-- faulty communication channel that forgets the ﬁrst bit, which can be mod-
-- elled using the tail function on lists of bits.
-- Answer in Hutton.Extended.Chapter07.TransmitExercise

-- 9. Deﬁne a function altMap :: (a -> b) -> (a -> b) -> [a] -> [b] that
-- alternately applies its two argument functions to successive elements in a list,
-- in turn about order. For example:
-- > altMap (+10) (+100) [0,1,2,3,4]  ---> [10,101,12,103,14]
altMap :: (a -> b) -> (a -> b) -> [a] -> [b]
altMap f g xs = [h k x | (k, x) <- zip [(0 :: Int) ..] xs]
  where h k y = if mod k 2 == 0 then f y else g y

-- 10. Using altMap, deﬁne a function luhn :: [Int] -> Bool that implements
-- the Luhn algorithm from the exercises in chapter 4 for bank card numbers of
-- any length. Test your new function using your own bank card.
luhnDouble :: Int -> Int
luhnDouble a | b < 10    = b
             | otherwise = b - 9
             where b = 2 * a

luhn :: [Int] -> Bool
luhn ns | mod addedUp 10 == 0 = True
        | otherwise           = False
        where addedUp = sum (altMap luhnDouble id ns)
