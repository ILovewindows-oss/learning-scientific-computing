module Hutton.Chapter06 where

-- 1. How does the recursive version of the factorial function behave if
-- applied to a negative argument, such as (-1)? Modify the deﬁnition to
-- prohibit negative arguments by adding a guard to the recursive case.
-- Note: Decided to use a different approach than the description.
-- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4247832/
factorial :: Int -> Int
factorial n | n < 0 = facnsign(n) * factorial (abs n) 
            | otherwise = foldr (*) 1 [1..n]
            where facnsign m = (-1)^(mod (abs m) 2)

-- 2. Deﬁne a recursive function sumdown :: Int -> Int that returns the sum
-- of the non-negative integers from a given value down to zero. For example,
-- sumdown 3 should return the result 3+2+1+0 “ 6 .
sumdown :: Int -> Int
sumdown 0 = 0
sumdown n = n + sumdown (n - 1)

-- 3. Deﬁne the exponentiation operator ^ for non-negative integers using the
-- same pattern of recursion as the multiplication operator *, and show how
-- the expression 2^3 is evaluated using your deﬁnition.
-- Note: Using alternative symbols here.
(*%) :: Int -> Int -> Int
_ *% 0 = 0
m *% n = m + (m *% (n-1))

(^%) :: Int -> Int -> Int
_ ^% 0 = 1
n ^% m = n *% (n ^% (m - 1))

-- 4. Deﬁne a recursive function euclid :: Int -> Int -> Int that implements
-- Euclid’s algorithm for calculating the greatest common divisor of two non-
-- negative integers: if the two numbers are equal, this number is the result;
-- otherwise, the smaller number is subtracted from the larger, and the same
-- process is then repeated. For example:
-- > euclid 6 27  ---> 3
euclid :: Int -> Int -> Int
euclid a b | a == b    = a
           | otherwise = euclid lo (hi - lo)
               where lo = min a b
                     hi = max a b

-- 6. Without looking at the deﬁnitions from the standard prelude, deﬁne the fol-
-- lowing library functions on lists using recursion.
-- a. Decide if all logical values in a list are True:
-- and :: [Bool] -> Bool
and' :: [Bool] -> Bool
and' []     = True
and' (x:xs) = x && (and' xs)

-- b. Concatenate a list of lists:
-- concat :: [[a]] -> [a]
concat' :: [[Int]] -> [Int]
concat' xs = [z | y <- xs, z <- y]

-- c. Produce a list with n identical elements:
-- replicate :: Int -> a -> [a]
replicate' :: Int -> Int -> [Int]
replicate' 0 _ = []
replicate' n a = a : replicate' (n - 1) a

-- d. Select the nth element of a list:
-- (!!) :: [a] -> Int -> a
(!!%) :: [Int] -> Int -> Int
[]     !!% _     = error "List must be at least `n` elements long"
(x:xs) !!% n
    | n < 0      = error "invalid negative indexing"
    | n > shape  = error (show n ++ " is above list length " ++ show shape)
    | n == 0     = x
    | otherwise  = xs !!% (n - 1)
        where shape = length [x:xs] + 1

-- e. Decide if a value is an element of a list:
-- elem :: Eq a => a -> [a] -> Bool
elem' :: Int -> [Int] -> Bool
elem' _ []     = False
elem' z (x:xs) = z == x || elem' z xs 

-- 7. Deﬁne a recursive function merge :: Ord a => [a] -> [a] -> [a] that
-- merges two sorted lists to give a single sorted list. For example:
-- > merge [2,5,6] [1,3,4]  ---> [1,2,3,4,5,6]
-- Note: your deﬁnition should not use other functions on sorted lists such as
-- insert or isort , but should be deﬁned using explicit recursion.
merge :: [Int] -> [Int] -> [Int]
merge xs [] = xs
merge [] ys = ys
merge (x:xs) (y:ys)
    | x < y     = x:(merge xs (y:ys))
    | otherwise = y:(merge (x:xs) ys)

-- 8. Using merge, deﬁne a function msort :: Ord a => [a] -> [a] that imple-
-- ments merge sort , in which the empty list and singleton lists are already
-- sorted, and any other list is sorted by merging together the two lists that
-- result from sorting the two halves of the list separately.
-- Hint: ﬁrst deﬁne a function halve :: [a] -> ([a],[a]) that splits a list
-- into two halves whose lengths diﬀer by at most one.
halve :: [Int] -> ([Int],[Int])
halve xs = (take n xs, drop n xs)
    where n = div (length xs) 2

msort :: [Int] -> [Int]
msort [ ] = [ ]
msort [x] = [x]
msort xs = merge (msort lower) (msort upper)
    where (lower, upper) = halve xs

-- 9. Using the ﬁve-step process, construct the library functions that:
-- a. calculate the sum of a list of numbers;
-- b. take a given number of elements from the start of a list;
-- c. select the last element of a non-empty list.
-- Note: I will be straight forward, not obeying the exercise

-- Step 1: define the type
-- sum' :: Num a => [a] -> a
-- Step 2: enumerate the cases
-- sum' [] =
-- sum' (x:xs) = 
-- Step 3: define the simple cases
-- sum' [] = 0
-- sum' (x:xs) = x + sum' xs
-- Step 4: define the other cases
-- N/A
-- Step 5: generalize and simplify
sum' :: [Int] -> Int
sum' [] = 0
sum' (x:xs) = x + sum' xs

-- Step 1: define the type
-- take' :: Int -> [a] -> [a]
-- Step 2: enumerate the cases
-- take' _ [] =
-- take' 0 xs =
-- take' n (x:xs) = 
-- Step 3: define the simple cases
-- take' _ [] = []
-- take' 0 xs = []
-- take' n (x:xs) = x:(take' (n-1) xs)
-- Step 4: define the other cases
-- N/A
-- Step 5: generalize and simplify
take' :: Int -> [Int] -> [Int]
take' _ []     = []
take' 0 _      = []
take' n (x:xs) = x : (take' (n-1) xs)

-- Step 1: define the type
-- last' :: [a] -> a
-- Step 2: enumerate the cases
-- last' [x] = 
-- last' (x:xs) = 
-- Step 3: define the simple cases
-- last' [x] = x
-- last' (x:xs) = last' xs
-- Step 4: define the other cases
-- N/A
-- Step 5: generalize and simplify
last' :: [Int] -> Int
last' []     = error "List must contain at least one element"
last' [x]    = x
last' (_:xs) = last' xs
