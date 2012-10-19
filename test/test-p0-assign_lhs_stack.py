#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p0-assign_lhs_stack.py
# Test Case
# Subset: p0
# Type: Official
# Tesing: LHS Stack Assignment
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

x = 1 + input()
y = x + x
z = y + y
w = z + z
a = w + w
b = a + a
c = b + b
d = c + c
e = d + d
f = x + y + z + w + a + b + c + d + e
print c
