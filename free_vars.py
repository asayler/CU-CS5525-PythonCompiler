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

STATIC_NAMES = ['True', 'False', 'add', 'is_int', 'is_bool', 'is_big',
                'inject_int', 'inject_bool', 'inject_big', 'project_int',
                'project_bool', 'project_big', 'equal', 'not_equal', 'error_pyobj',
                'print_any', 'is_true', 'input', 'input_int']

class FreeVarsVisitor(SetVisitor):
    def __init__(self):
        super(FreeVarsVisitor,self).__init__()
        self.local_visitor = LocalVarsVisitor()

    def visitAssign(self, n):
        return self.dispatch(n.expr) - reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.nodes), 
                                              set([]))

    def visitName(self, n):
        if n.name in STATIC_NAMES:
            return set([])
        else: return set([name(n)])

    def visitAssName(self, n):
        return set([name(n)])

    # Non-Terminal Expressions

    def visitLet(self, n):
        return self.dispatch(n.rhs) | (self.dispatch(n.body) - self.dispatch(n.var))

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
