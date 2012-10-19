#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p1-IfExpAdd.py
# Test Case
# Subset: p1
# Type: Student
# Tesing: IfExp/Add
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

x = 1
print(x)
y = 2
print(y)
z = x + y
print(z)
x = 4 if z else 0
print(x)
y = 0 if 0 else 5
print(y)
z = 6
print(z)
