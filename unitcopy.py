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
        return mono_Module(n.doc, self.dispatch(n.node), n.lineno)

    # Statements    

    def visitStmt(self, n):
        nodes = []
        for s in n.nodes:
            nodes += [self.dispatch(s)]
        return mono_Stmt(nodes, n.lineno)

    def visitPrintnl(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return mono_Printnl(nodes, n.dest, n.lineno)

    def visitAssign(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return mono_Assign(nodes, self.dispatch(n.expr), n.lineno)
    
    def visitDiscard(self, n):
        return mono_Discard(self.dispatch(n.expr), n.lineno)
    
    # Terminal Expressions

    def visitConst(self, n):
        return mono_Const(n.value, n.lineno)

    def visitName(self, n):
        return mono_Name(n.name, n.lineno)

    def visitAssName(self, n):
        return mono_AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)];
        return mono_List(nodes, n.lineno)

    def visitDict(self, n):
        items = []
        for item in n.items:
            items += [self.dispatch(item)];
        return mono_Dict(items, n.lineno)

    def visitSubscript(self, n):
        return mono_Subscript(self.dispatch(n.expr), n.flags, n.subs, n.lineno)
        
    def visitCompare(self, n):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1]))
            ops += [newop]
        return mono_Compare(self.dispatch(n.expr), ops, n.lineno)

    def visitAdd(self, n):
        return mono_Add((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)
        
    def visitOr(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return mono_Or(nodes, n.lineno)

    def visitAnd(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return mono_And(nodes, n.lineno)

    def visitNot(self, n):
        return mono_Not(self.dispatch(n.expr), n.lineno)

    def visitUnarySub(self, n):
        return mono_UnarySub(self.dispatch(n.expr), n.lineno())

    def visitIfExp(self, n):
        return mono_IfExp(self.dispatch(n.test),
                          self.dispatch(n.then),
                          self.dispatch(n.else_),
                          n.lineno)    

    def visitCallFunc(self, n):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return mono_CallFunc(self.dispatch(n.node), args, n.star_args, n.dstar_args, n.lineno)
