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

class SetVisitor(Visitor):

    # Modules

    def visitModule(self, n):
        if isinstance(n.node, list):
            return reduce(lambda x,y: x | y, map(self.dispatch, n.node), 
                          set([]))
        else:
            return self.dispatch(n.node)

    # Statements    

    def visitStmt(self, n):
        lvs = set([])
        for s in n.nodes:
            lvs = lvs | self.dispatch(s)
        return lvs

    def visitAssign(self, n):
        return self.dispatch(n.expr) | reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.nodes), 
                                              set([]))
        
    def visitDiscard(self, n):
        return self.dispatch(n.expr)

    def visitIf(self, n):
        return self.dispatch(n.else_) | reduce(lambda x,y: x | y,
                                               map(lambda (x,y): self.dispatch(x) | self.dispatch(y),
                                                   n.tests),
                                               set([]))

    # Terminal Expressions

    def visitConst(self, n):
        return set([])

    def visitName(self, n):
        return set([])

    def visitAssName(self, n):
        return set([])
    
    def visitString(self, n):
        return set([])

    def visitInstrSeq(self, n):
        return self.dispatch(n.expr) | reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.nodes), 
                                              set([]))

    # Non-Terminal Expressions

    def visitAdd(self, n):
        return self.binary(n)

    def visitCallFunc(self, n):
        return self.dispatch(n.node) | reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.args), 
                                              set([]))
    def visitIndirectCallFunc(self, n):
        return self.dispatch(n.node) | reduce(lambda x,y: x | y, 
                                              map(self.dispatch, n.args), 
                                              set([]))

    def visitCompare(self, n):
        ls = set([])
        for op in n.ops:
            ls = ls | self.dispatch(op[1])
        return ls

    def binary(self, n):
        return self.dispatch(n.left) | self.dispatch(n.right)

    def visitAdd(self, n):
        return self.binary(n)

    def visitIntAdd(self, n):
        return self.binary(n)

    def visitEqual(self, n):
        return self.binary(n)    

    def visitIntEqual(self, n):
        return self.binary(n)

    def visitNotEqual(self, n):
        return self.binary(n)

    def visitIntNotEqual(self, n):
        return self.binary(n)

    def visitSLambdaLabel(self, n):
        return set([])

    def visitIntUnarySub(self, n):
        return self.dispatch(n.expr)

    def visitUnarySub(self, n):
        return self.dispatch(n.expr)

    def visitGetattr(self, n):
        return self.dispatch(n.expr)

    def visitNot(self, n):
        return self.dispatch(n.expr)

    def visitLet(self, n):
        return self.dispatch(n.var) | (self.dispatch(n.rhs) | self.dispatch(n.body))
    
    def visitIfExp(self, n):
        return self.dispatch(n.test) | self.dispatch(n.then) | self.dispatch(n.else_)

    def visitLambda(self, n):
        return self.dispatch(n.code)

    def visitSLambda(self, n):
        return self.dispatch(n.code)

    def visitPrintnl(self, n):
        return reduce(lambda x,y: x | y, map(self.dispatch, n.nodes), set([]))

    def visitList(self, n):
        return reduce(lambda x,y: x | y, map(self.dispatch, n.nodes), set([]))

    def visitDict(self, n):
        return reduce(lambda x,y: x | y, map(lambda (_,z): self.dispatch(z), n.items), set([]))

    def visitIsTag(self, n):
        return self.dispatch(n.arg)

    def visitProjectTo(self, n):
        return self.dispatch(n.arg)

    def visitInjectFrom(self, n):
        return self.dispatch(n.arg)

    def visitAnd(self, n):
        return reduce(lambda x,y: x | y, map(self.dispatch, n.nodes), set([]))

    def visitOr(self, n):
        return reduce(lambda x,y: x | y, map(self.dispatch, n.nodes), set([]))

    def visitSubscript(self, n):
        return self.dispatch(n.expr) | reduce(lambda x,y: x | y, map(self.dispatch, n.subs), set([]))

    def visitSubscriptAssign(self, n):
        return self.dispatch(n.target) | self.dispatch(n.value) | self.dispatch(n.sub)

    def visitAttrAssign(self, n):
        return self.dispatch(n.target) | self.dispatch(n.value)

    def visitReturn(self, n):
        return self.dispatch(n.value)

    def visitWhile(self, n):
        return self.dispatch(n.test) | self.dispatch(n.body) 

    def visitWhileFlat(self, n):
        return self.dispatch(n.testss) | self.dispatch(n.test) | self.dispatch(n.body) | (self.dispatch(n.else_) if n.else_ else set([]))

    def visitClass(self, n):
        return self.dispatch(n.code) | reduce(lambda x,y: x | y, map(self.dispatch, n.bases), set([]))