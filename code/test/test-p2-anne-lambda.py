#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-anne-lambda.py
# Test Case
# Subset: p2
# Type: Student
# Tesing: Lambda
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

x = lambda a: a + 3
print x(4)
y = lambda b,x: b + x
print y(3,5)
a = [3,4,5]
b = [6,7,8]
print y(a,b)
