#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p3-whileloop3.py
# Test Case
# Subset: p3
# Type: Student
# Tesing: Nested while loops w/ if expressions
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

x = 3
while(x):
    y = 3
    while(y):
        print((x + -y) if x == 2 else 9)
        y = y + -1
    x = x + -1
