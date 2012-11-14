#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-issue3.py
# Test Case
# Subset: p3
# Type: Student
# Tesing: Github Issue #3
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

def f():
    def getx():
        return 10
    return getx if input() else getx

f()
f()
