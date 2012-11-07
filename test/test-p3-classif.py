#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p3-whileloop1.py
# Test Case
# Subset: p3
# Type: Student
# Tesing: while loops
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

class M:
    if input():
        x = 10
    else:
        x = 20

class N:
    if input():
        x = 10
    else:
        x = 20

print M.x
print N().x
