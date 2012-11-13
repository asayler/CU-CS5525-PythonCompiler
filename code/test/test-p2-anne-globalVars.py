#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-anne-globalVars.py
# Test Case
# Subset: p2
# Type: Student
# Tesing: Global vars
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

x = 1
y = 2
z = 3
x_1 = 4
print0 = 5
print_0 = x
print 6
print print_0

def f(y):
	x = 7
	y = 42
	a = b + 2
	c = 2
	y = c + 5
	print x
	return 0

print x
b = [8,9,10]
b[1] = 11
