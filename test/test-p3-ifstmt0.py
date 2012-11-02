#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p1-ifexp0.py
# Test Case
# Subset: p1
# Type: Official
# Tesing: Subscripts/Lists
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

if (0 if 1 else 2):
    print 2
    print 4
else:
    print 8
    print 10
