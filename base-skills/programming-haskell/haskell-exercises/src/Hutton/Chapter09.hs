module Hutton.Chapter09 where

-- 1. Redeﬁne the combinatorial function choices using a list comprehension rather
-- than using composition, concat and map.


-- 2. Deﬁne a recursive function isChoice :: Eq a => [a] -> [a] -> Bool that
-- decides if one list is chosen from another, without using the combinatorial
-- functions perms and subs. Hint: start by deﬁning a function that removes the
-- ﬁrst occurrence of a value from a list.


-- 3. What eﬀect would generalising the function split to also return pairs con-
-- taining the empty list have on the behaviour of solutions?
-- 4. Using the functions choices, exprs, and eval, verify that there are 33665406
-- possible expressions over the numbers 1, 3 , 7 , 10 , 25 , 50, and that only 4672540
-- of these expressions evaluate successfully.


-- 5. Similarly, verify that the number of expressions that evaluate successfully
-- increases to 10,839,369 if the numeric domain is generalised to arbitrary in-
-- tegers. Hint: modify the deﬁnition of valid.


-- 6. Modify the ﬁnal program to:
-- a. allow the use of exponentiation in expressions;
-- b. produce the nearest solutions if no exact solution is possible;
-- c. order the solutions using a suitable measure of simplicity.
