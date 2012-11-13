#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p3-WhileIf1.py
# Test Case
# Subset: p3
# Type: Student
# Tesing: Basic While Loop with Nested If Statments
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

x = 3
while(x):
    if(x == 3):
        print False
    else:
        if(x == 2):
            print True
        else:
            if(x == 1):
                print False
            else:
                print 0
    x = x + -1
