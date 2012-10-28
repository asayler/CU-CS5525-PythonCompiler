#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-fun3.py
# Test Case
# Subset: p2
# Type: Official
# Tesing: return functions
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

def f(x):
    y = 4
    return lambda z: x + y + z

f1 = f(1)
print f1(3)
