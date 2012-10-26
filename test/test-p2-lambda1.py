#!/usr/bin/python

adder = lambda x: (lambda y: x + y)
add5 = adder(5)
seventeen = add5(12)
print seventeen
