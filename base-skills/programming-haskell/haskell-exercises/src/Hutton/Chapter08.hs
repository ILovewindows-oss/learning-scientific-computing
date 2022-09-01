module Hutton.Chapter08 where

-- 1. In a similar manner to the function add, deﬁne a recursive multiplication
-- function mult :: Nat -> Nat -> Nat for the recursive type of natural numbers:
-- Hint: make use of add in your deﬁnition.


-- 2. Although not included in appendix B, the standard prelude deﬁnes
-- > data Ordering = LT | EQ | GT
-- together with a function
-- > compare :: Ord a => a -> a -> Ordering
-- that decides if one value in an ordered type is less than (LT), equal to (EQ),
-- or greater than (GT) another value. Using this function, redeﬁne the function
-- > occurs :: Ord a => a -> Tree a -> Bool for search trees. Why is this
-- new deﬁnition more eﬃcient than the original version?


-- 3. Consider the following type of binary trees:
-- > data Tree a = Leaf a | Node (Tree a) (Tree a)
-- Let us say that such a tree is balanced if the number of leaves in the left and
-- right subtree of every node diﬀers by at most one, with leaves themselves be-
-- ing trivially balanced. Deﬁne a function balanced :: Tree a -> Bool that
-- decides if a binary tree is balanced or not.
-- Hint: ﬁrst deﬁne a function that returns the number of leaves in a tree.


-- 4. Deﬁne a function balance :: [a] -> Tree a that converts a non-empty
-- list into a balanced tree. Hint: ﬁrst deﬁne a function that splits a list into
-- two halves whose length diﬀers by at most one.


-- 5. Given the type declaration
-- > data Expr = Val Int | Add Expr Expr
-- deﬁne a higher-order function
-- > folde :: (Int -> a) -> (a -> a -> a) -> Expr -> a
-- such that folde f g replaces each Val constructor in an expression by the
-- function f, and each Add constructor by the function g.


-- 6. Using folde, deﬁne a function eval :: Expr -> Int that evaluates an ex-
-- pression to an integer value, and a function size :: Expr -> Int that cal-
-- culates the number of values in an expression.


-- 7. Complete the following instance declarations:
-- > instance Eq a => Eq (Maybe a) where
-- > ...
-- > instance Eq a => Eq [a] where
-- > ...


-- 8. Extend the tautology checker to support the use of logical disjunction (_)
-- and equivalence (ô) in propositions.


-- 9. Extend the abstract machine to support the use of multiplication.
