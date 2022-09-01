module Hutton.Chapter05 where

-- 1. Using a list comprehension, give an expression that calculates the sum
-- 1^2 + 2^2 + ... + 100^2 of the ﬁrst one hundred integer squares.
sumSq :: Int -> Int -> Int
sumSq a b = sum [x * x | x <- [a..b]]

-- 2. Suppose that a coordinate grid of size m x n is given by the list of all
-- pairs p x, y q of integers such that 0 \le x \le m and 0 \le y \le n. Using
-- a list comprehension, deﬁne a function grid :: Int -> Int -> [(Int,Int)]
-- that returns a coordinate grid of a given size. For example:
-- > grid 1 2  ---> [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]
grid :: Int -> Int -> [(Int, Int)]
grid m n = [(x, y) | x <- [0..m], y <- [0..n]]

-- 3. Using a list comprehension and the function grid above, deﬁne a function
-- square :: Int -> [(Int,Int)] that returns a coordinate square of size n,
-- excluding the diagonal from p 0 , 0 q to p n, n q . For example:
-- > square 2  ---> [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]
square :: Int -> [(Int, Int)]
square n = [(x, y) | (x, y) <- grid n n, x /= y]

-- 4. In a similar way to the function length, show how the library function
-- replicate :: Int -> a -> [a] that produces a list of identical elements
-- can be deﬁned using a list comprehension. For example:
-- > replicate 3 True  ---> [True,True,True]
replicate' :: Int -> a -> [a]
replicate' n a = [a | _ <- [1..n]]

-- 5. A triple p x, y, z q of positive integers is Pythagorean if it satisﬁes
-- the equation x^2 + y^2 = z^2 . Using a list comprehension with three
-- generators, deﬁne a function pyths :: Int -> [(Int,Int,Int)] that returns
-- the list of all such triples whose components are at most a given limit.
-- For example:
-- > pyths 10  -- [(3,4,5),(4,3,5),(6,8,10),(8,6,10)]
pyths :: Int -> [(Int, Int, Int)]
pyths n = [(x, y, z) | x <- [1..n], y <- [1..n], z <- [1..n], x*x + y*y == z*z]

-- 6. A positive integer is perfect if it equals the sum of all of its factors,
-- excluding the number itself. Using a list comprehension and the function
-- factors, deﬁne a function perfects :: Int -> [Int] that returns the list of
-- all perfect numbers up to a given limit. For example:
-- > perfects 500  ---> [6,28,496]
perfects :: Int -> [Int]
perfects n = [x | x <- [1..n], isPerfect x]
    where
        isPerfect m = sum (factors m) == 2 * m
        factors m = [x | x <- [1..m], mod m x == 0]

-- 7. Show how the list comprehension [(x,y) | x <- [1,2], y <- [3,4]] with
-- two generators can be re-expressed using two comprehensions with single gen-
-- erators. Hint: nest one comprehension within the other and make use of the
-- library function concat :: [[a]] -> [a].
-- lcRef :: (Num a, Num b) => [(a, b)]
-- lcRef = [(x, y) | x <- [1, 2], y <- [3, 4]]
nestedlc :: [Int] -> [Int] -> [(Int, Int)]
nestedlc xs ys = concat [[(x, y) | y <- ys] | x <- xs]

-- 8. Redeﬁne the function positions using the function find.
-- positions :: Eq a => a -> [a] -> [Int]
-- positions x xs = [i | (x', i) <- zip xs [0..], x == x']
positions :: Int -> [Int] -> [Int]
positions x xs = find x (zip xs [0..])
    where find k t = [v | (k', v) <- t, k == k']

-- The scalar product of two lists of integers xs and ys of length n is given
-- by the sum of the products of corresponding integers:
--     \sum_{i=0}^{n-1} x_{i}y_{i}
-- In a similar manner to chisqr, show how a list comprehension can be used to
-- deﬁne a function scalarproduct :: [Int] -> [Int] -> Int that returns
-- the scalar product of two lists. For example:
-- > scalarproduct [1,2,3] [4,5,6]  ---> 32
scalarproduct :: [Int] -> [Int] -> Int
scalarproduct vs ws = sum [v * w | (v, w) <- zip vs ws]

-- TODO 10. Modify the Caesar cipher program to also handle upper-case letters.
