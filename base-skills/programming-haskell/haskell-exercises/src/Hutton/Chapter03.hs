module Hutton.Chapter03 where

-- 2. Write down deﬁnitions that have the following types; it does not matter
-- what the deﬁnitions actually do as long as they are type correct.
bools :: [Bool]
bools = [True, False, True]

nums :: [[Int]]
nums = [[x :: Int] | x <- [0..10]]

add :: Int -> Int -> Int -> Int
add x y z = sum [b :: Int | b <- [x, y, z]]

copy :: b -> (b, b)
copy a = (a, a)

apply :: (t1 -> t2) -> t1 -> t2
apply f x = f(x)

-- 3. What are the types of the following functions?
second :: [a] -> a
second xs = head (tail xs)

swap :: (b, a) -> (a, b)
swap (x, y) = (y, x)

pair :: a -> b -> (a, b)
pair x y = (x, y)

double :: Num a => a -> a
double x = 2 * x

palindrome :: Eq a => [a] -> Bool
palindrome xs = reverse xs == xs

twice :: (t -> t) -> t -> t
twice f x = f (f x)
