# CU CS5525
# Fall 2012
# Python Compiler
#
# find_locals.py
# Visitor Funstions to Find Local Variables
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

from pyast import *
from set_visitor import SetVisitor

def name(n):
    if isinstance(n, Name) or isinstance(n, AssName):
        return n.name
    else: raise Exception('Getting name of invalid node ' + str(n))

class FindLocalsVisitor(SetVisitor):

    def visitClass(self, n):
        return set([n.name])

    def visitFunction(self, n):
        return set([n.name])

    def visitVarAssign(self, n):
        return set([n.target])
