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
from vis import Visitor

DISCARDTEMP = "discardtemp"
NULLTEMP = "nulltemp"
IFTEMP = "iftemp"

IfThenLabelCnt = 0
ELSELABEL  = "else"
ENDIFLABEL = "endelse"

def name(n):
    if isinstance(n, Name) or isinstance(n, AssName):
        return n.name
    else: raise Exception('Getting name of invalid node ' + str(n))

class InstrSelectVisitor(Visitor):

    # Modules

    def visitModule(self, n):
        return self.dispatch(n.node)

    # Statements    

    def visitStmt(self, n):
        lvs = set([])
        for s in n.nodes:
            lvs = fvs | self.dispatch(s)
        return lvs

    def visitAssign(self, n):
        return self.dispatch(n.expr) - reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.nodes), 
                                              set([]))
        
    def visitDiscard(self, n):
        return self.dispatch(n.expr)
    
    # Terminal Expressions

    def visitConst(self, n):
        return set([])

    def visitName(self, n):
        if n.name == 'True' or n.name == 'False':
            return set([])
        else: return set([name(n)])

    def visitAssName(self, n):
        return set([name(n)])

    # Non-Terminal Expressions

    def visitCallFunc(self, n):
        return self.dispatch(n.node) | reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.args), 
                                              set([]))

    def binary(self, n):
        return self.dispatch(n.left) | self.dispatch(n.right)

    def visitIntAdd(self, n):
        return self.binary(n)
    def visitIntEqual(self, n):
        return self.binary(n)
    def visitIntNotEqual(self, n):
        return self.binary(n)

    def visitIntUnarySub(self, n):
        return self.dispatch(n.expr)

    def visitLet(self, n):
        return self.dispatch(n.rhs) | (self.dispatch(n.body) - self.dispatch(n.name))
    
    def visitIfExp(self, n):
        return self.dispatch(n.test) | self.dispatch(n.then) | self.dispatch(n.else_)

    def visitSLambda(self, n):
        return self.dispatch(n.code) - set(n.params)
