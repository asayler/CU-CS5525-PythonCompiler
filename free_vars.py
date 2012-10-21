# CU CS5525
# Fall 2012
# Python Compiler
#
# instr_select.py
# Visitor Funcations for x86 Instruction Selection
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

import sys

# Data Types
from compiler.ast import *
from monoast import *

# Helper Tools
from set_visitor import SetVisitor

def name(n):
    if isinstance(n, Name) or isinstance(n, AssName):
        return n.name
    else: raise Exception('Getting name of invalid node ' + str(n))

class FreeVarsVisitor(SetVisitor):
    def __init__(self):
        super(FreeVarsVisitor,self).__init__()
        self.local_visitor = LocalVarsVisitor()

    def visitAssign(self, n):
        return self.dispatch(n.expr) - reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.nodes), 
                                              set([]))

    def visitName(self, n):
        if n.name == 'True' or n.name == 'False':
            return set([])
        else: return set([name(n)])

    def visitAssName(self, n):
        return set([name(n)])

    # Non-Terminal Expressions

    def visitLet(self, n):
        return self.dispatch(n.rhs) | (self.dispatch(n.body) - self.dispatch(n.name))

    def visitSLambda(self, n):
        n.free_vars = self.dispatch(n.code) - (set(n.params) | self.local_visitor.preorder(n.code)) 
        return n.free_vars

class LocalVarsVisitor(SetVisitor):
    def visitSLambda(self, n):
        n.local_vars = self.dispatch(n.code) - set(n.params)
        return set([])

    def visitAssName(self, n):
        return set([name(n)])

class NestedFreeVarsVisitor(SetVisitor):
    def visitSLambda(self, n):
        return n.free_vars
