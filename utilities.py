# CU CS5525
# Fall 2012
# Python Compiler
#
# utilities.py
# Compiler Utility Functions
#
# Adopted from code by Jeremy Siek, Fall 2012
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

from compiler.ast import *

counter = 1

def generate_name(x):
    global counter
    name = str(counter) + '_' + x
    counter = counter + 1
    return name

def make_assign(lhs, rhs):
    return Assign(nodes=[AssName(name=lhs, flags='OP_ASSIGN')], expr=rhs)
