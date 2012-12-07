#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p0-1.py
# Test Case
# Subset: p0
# Type: Student
# Tesing: input, usub, add, print
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


def square(x):
    cnt = x
    val = 0
    while(cnt != 0):
        val = val + x
        cnt = cnt + -1
    return val

print(square(input()))
