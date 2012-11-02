# CU CS5525
# Fall 2012
# Python Compiler
#
# unitcopy.py
# Unit Copy Visitor Functions
# Used as template for other visitors
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

    def visitIf(self, n):
        return If(map(lambda (x,y): (self.dispatch(x), self.dispatch(y)), 
                      n.tests),
                  self.dispatch(n.else_))
    
    def visitDiscard(self, n):
        return Discard(self.dispatch(n.expr), n.lineno)
    
    def visitFunction(self, n):
        return Function(n.decorators, n.name, n.argnames, n.defaults,
                        n.flags, n.doc, self.dispatch(n.code))

    # Terminal Expressions

    def visitConst(self, n):
        return Const(n.value, n.lineno)

    def visitName(self, n):
        return Name(n.name, n.lineno)

    def visitAssName(self, n):
        return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitLambda(self, n):
        return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code))

    def visitReturn(self, n):
        return Return(self.dispatch(n.value))

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return List(nodes, n.lineno)

    def visitDict(self, n):
        items = []
        for item in n.items:
            key = self.dispatch(item[0])
            value = self.dispatch(item[1])
            items += [(key, value)]
        return Dict(items, n.lineno)

    def visitSubscript(self, n):
        expr = self.dispatch(n.expr)
        subs = []
        for sub in n.subs:
            subs += [self.dispatch(sub)]
        return Subscript(expr, n.flags, subs, n.lineno)
    
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
        return UnarySub(self.dispatch(n.expr), n.lineno)

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

    def visitCallFunc(self, n):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return CallFunc(self.dispatch(n.node), args, n.star_args, n.dstar_args, n.lineno)
