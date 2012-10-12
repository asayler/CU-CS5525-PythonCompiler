#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# unit copy visitor functions to use as template for other visitors
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys

# Data Types
from compiler.ast import *
from monoast import *

# Helper Tools
from vis import Visitor

class CopyVisitor(Visitor):

    # Modules

    def visitModule(self, n):
        return Module(n.doc, self.dispatch(n.node), n.lineno)

    # Statements    

    def visitStmt(self, n):
        nodes = []
        for s in n.nodes:
            nodes += [self.dispatch(s)]
        return Stmt(nodes, n.lineno)

    def visitPrintnl(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Printnl(nodes, n.dest, n.lineno)

    def visitAssign(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Assign(nodes, self.dispatch(n.expr), n.lineno)
    
    def visitDiscard(self, n):
        return Discard(self.dispatch(n.expr), n.lineno)
    
    # Terminal Expressions

    def visitConst(self, n):
        return Const(n.value, n.lineno)

    def visitName(self, n):
        return Name(n.name, n.lineno)

    def visitAssName(self, n):
        return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return List(nodes, n.lineno)

    def visitDict(self, n):
        items = []
        for item in n.items:
            items += [self.dispatch(item)]
        return Dict(items, n.lineno)

    def visitSubscript(self, n):
        return Subscript(self.dispatch(n.expr), n.flags, n.subs, n.lineno)
        
    def visitCompare(self, n):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1]))
            ops += [newop]
        return Compare(self.dispatch(n.expr), ops, n.lineno)

    def visitAdd(self, n):
        return Add((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)
        
    def visitOr(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Or(nodes, n.lineno)

    def visitAnd(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return And(nodes, n.lineno)

    def visitNot(self, n):
        return Not(self.dispatch(n.expr), n.lineno)

    def visitUnarySub(self, n):
        return UnarySub(self.dispatch(n.expr), n.lineno())

    def visitIfExp(self, n):
        return IfExp(self.dispatch(n.test),
                          self.dispatch(n.then),
                          self.dispatch(n.else_),
                          n.lineno)    

    def visitCallFunc(self, n):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return CallFunc(self.dispatch(n.node), args, n.star_args, n.dstar_args, n.lineno)
