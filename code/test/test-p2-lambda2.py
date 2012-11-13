#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-fun3.py
# Test Case
# Subset: p2
# Type: 
# Tesing: 
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

adder = lambda x: (lambda y: input() + x + y)
add5andinput = adder(5)
over14 = add5andinput(9)
print over14
