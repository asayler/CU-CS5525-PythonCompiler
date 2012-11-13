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
y = 10
z = 50
class B:
    print y
    x = 80
    y = 20
    print y
    print x
    print z
    def f(self, m):
        return self.y

print B().f(33)
print B.f(B(), 99)
