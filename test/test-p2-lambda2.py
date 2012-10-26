#!/usr/bin/python

adder = lambda x: (lambda y: input() + x + y)
add5andinput = adder(5)
over14 = add5andinput(9)
print over14
