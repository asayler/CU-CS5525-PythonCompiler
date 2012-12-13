#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-benchmark-squareloop.py
# Test Case
# Subset: Benchmark
# Type: Student
# Testing: Benchmark
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

n = input()
i = 0
while i != square(n):
    j = 0
    while j != n:
        square(n)
        j = j + 1
    i = i + 1
