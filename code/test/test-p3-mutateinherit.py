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

class D:
    y = 30
    h = 10

class B(D):
    x = 80
    y = 20
    def f(self, m):
        print self.y
        print self.h
        print self.x

b = B()
bf = b.f
bf(3)
D.h = 70
B.x = 90
b.y = 110
Bf = B.f
Bf(b, 70)
