#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-anne-funcsWithInsert.py
# Test Case
# Subset: p2
# Type: Student
# Tesing: Funcs with input
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

z = 3
def f(x, g):
	x = lambda g: g + input()
	print x(5)
	return 0
print f(3, 6)
