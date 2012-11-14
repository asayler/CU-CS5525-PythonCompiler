#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-issues1-1.py
# Test Case
# Subset: p1
# Type: Student
# Tesing: Github Issue 1
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

b = 3
def sum(x):
 y = 2
 b = 5
 b = 6
 print x + y
 a = mul(y)
 return lambda x: x + 4 + y
 
def mul(t):
 return t + -t 

print sum(2)(3)
