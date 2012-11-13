#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p0-liveness1.py
# Test Case
# Subset: p0
# Type: Student
# Tesing: Reg Alloc Liveness Analysis
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

z = 4
w = 0
z = 1
x = w + z
y = w + x
w = y + x
