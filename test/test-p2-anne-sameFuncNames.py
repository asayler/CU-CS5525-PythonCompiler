#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-p2-anne-sameFuncNames.py
# Test Case
# Subset: p2
# Type: Student
# Tesing: Same Func Names
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

def x(a):
	def x(b, c):
		return b+c
	return(x(a,1))

print x(3)
