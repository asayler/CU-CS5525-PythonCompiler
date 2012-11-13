#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-fun3.py
# Test Case
# Subset: p2
# Type: 
# Tesing: recursion
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

def countto_iter(x, limit):
    print x
    return (x if x == limit else countto_iter(x + 1, limit))

def countto(limit):
    return countto_iter(0, limit)

countto(12)
countto(input())
