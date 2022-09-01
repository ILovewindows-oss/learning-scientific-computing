module Hutton.Chapter02 where

-- 4. The library function last selects the last element of a non-empty list;
-- for example, last [1,2,3,4,5] “ 5. Show how the function last could be deﬁned
-- in terms of the other library functions introduced in this chapter. Can you
-- think of another possible deﬁnition?
last' :: [Int] -> Int
last' xs = head (reverse xs)

-- 5. The library function init removes the last element from a non-empty list;
-- for example, init [1,2,3,4,5] “ [1,2,3,4] . Show how init could similarly
-- be deﬁned in two diﬀerent ways.
init' :: [Int] -> [Int]
init' xs = take (length xs -1) xs

init'' :: [Int] -> [Int]
init'' xs = reverse (tail (reverse xs))
