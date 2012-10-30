#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-fu1.py
# Test Case
# Subset: p2
# Type: 
# Tesing: 
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

def mult(x, y):
    return 0 if x == 0 else (y if x == 1 else y + mult(x + -1, y))

def fact(x):
    return 1 if x == 1 else mult(x, fact(x + -1))

print fact(5)
