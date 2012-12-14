#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-benchmark-pi0.py
# Test Case
# Subset: benchmark
# Type: Student
# Tesing: benchmark
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
    return mul(x, x)

def mul(x, y):
    cnt = x
    val = 0
    while(cnt != 0):
        val = val + y
        cnt = cnt + -1
    return val

cnto = input()
cnti = input()
y = input()
while(cnto != 0):
    while(cnti != 0):
        print(square(y))
        cnti = cnti + -1
    cnto = cnto + -1
