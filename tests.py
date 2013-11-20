#!/usr/bin/python
from __future__ import division

from functools import lru_cache
from persistent_lru_cache import persistent_lru_cache

import timeit

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

@persistent_lru_cache(filename='fib.db', maxsize=None)
def pfib(n):
    if n < 2:
        return n
    return pfib(n-1) + pfib(n-2)

t0 = timeit.timeit(lambda: fib(100), number=100000)
t1 = timeit.timeit(lambda: pfib(100), number=100000)
print(t0, t1)
print(fib.cache_info(), pfib.cache_info())

import urllib
import urllib.error, urllib.request

def get_pep(num):
    'Retrieve text of a Python Enhancement Proposal'
    resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
    try:
        with urllib.request.urlopen(resource) as s:
            return s.read()
    except urllib.error.HTTPError:
        return 'Not Found'

l_get_pep = lru_cache(maxsize=32)(get_pep)
p_get_pep = persistent_lru_cache(filename='pep.pickle', maxsize=32)(get_pep)

peps = 8, 290 #, 308, 320, 8, 218, 320, 279, 289, 320, 9991
#t0 = timeit.timeit(lambda: [len(get_pep(pep)) for pep in peps], number=3)
t1 = timeit.timeit(lambda: [len(l_get_pep(pep)) for pep in peps], number=3)
t2 = timeit.timeit(lambda: [len(p_get_pep(pep)) for pep in peps], number=3)

print(t0, t1, t2)

# TODO: Write unit tests instead of this quick&dirty timing test followed
# by tests copied from another module...

import unittest

class TestPersistentLruCache(unittest.TestCase):
    def test_foldl(self):
        self.assertEqual(foldl(truediv, 1, [2, 3, 4]), 1/2/3/4)
        self.assertEqual(foldl1(truediv, [1, 2, 3, 4]), 1/2/3/4)
    def test_foldr(self):
        self.assertEqual(foldr(truediv, 4, [1, 2, 3]), 1/(2/(3/4)))
        self.assertEqual(foldr1(truediv, [1, 2, 3, 4]), 1/(2/(3/4)))
    def test_scanl(self):
        self.assertEqual(list(scanl(truediv, 1, [2, 3, 4])),
                         [1, 1/2, 1/2/3, 1/2/3/4])
        self.assertEqual(list(scanl1(truediv, [1, 2, 3, 4])),
                         [1, 1/2, 1/2/3, 1/2/3/4])
    def test_scanr(self):
        self.assertEqual(list(scanr(truediv, 4, [1, 2, 3])),
                         [1/(2/(3/4)), 2/(3/4), 3/4, 4])
        self.assertEqual(list(scanr1(truediv, [1, 2, 3, 4])), 
                         [1/(2/(3/4)), 2/(3/4), 3/4, 4])
    def test_empty(self):
        self.assertEqual(foldl(truediv, 0, []), 0)
        self.assertRaises(TypeError, foldl1, truediv, [])
        self.assertEqual(foldr(truediv, 0, []), 0)
        self.assertRaises(TypeError, foldr1, truediv, [])
        self.assertEqual(list(scanl(truediv, 0, [])), [0])
        self.assertEqual(list(scanl1(truediv, [])), [])
        self.assertEqual(list(scanr(truediv, 0, [])), [0])
        self.assertEqual(list(scanr1(truediv, [])), [])

class TestConst(unittest.TestCase):
    def test_const(self):
        c1 = const(5)
        c2 = constantly(5)(None)
        self.assertEqual(c1, c2)

class TestCompose(unittest.TestCase):
    def test_no_args(self):
        f = compose()
        self.assertEqual(f(3), 3)
    def test_one_arg(self):
        f = compose(truediv)
        self.assertEqual(f(1, 2), 1/2)
    def test_two_args(self):
        f = compose(lambda x: 1/x, truediv)
        self.assertEqual(f(1, 2), 2)
        f = compose(truediv, lambda x, y: (y, x), unpack=True)
        self.assertEqual(f(1, 2), 2)
    def test_three_args(self):
        f = compose(lambda x:-x, lambda x:1/x, truediv)
        self.assertEqual(f(1, 2), -2)
        f = compose(truediv, lambda x, y: (y, x), lambda x: (x, x/2), unpack=True)
        self.assertEqual(f(1), 1/2)
    def test_bad_args(self):
        f = compose(lambda x: 1/x, None, truediv)
        self.assertRaises(TypeError, f, 1, 2)

class TestNullable(unittest.TestCase):
    def test_nullable(self):
        nulldiv = nullable(truediv)
        self.assertEqual(nulldiv(1, 2), 1/2)
        self.assertEqual(nulldiv(1, None), None)
        self.assertEqual(nulldiv(None, 2), None)
        self.assertEqual(nulldiv(None, None), None)
        self.assertRaises(TypeError, nulldiv, 1, 'a')
    def todo_nullable_badargs(self):
        nulldiv = nullable(truediv)
        self.assertRaises(TypeError, nulldiv, None)
        self.assertRaises(TypeError, nulldiv, 1, None, 2)
            
#if __name__ == '__main__':
#    unittest.main()
