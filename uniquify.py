# CU CS5525
# Fall 2012
# Python Compiler
#
# uniquify.py
# Visitor Funstions to Uniquify AST
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

import sys
import copy

# Data Types
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

debug = True

class UniquifyVisitor(CopyVisitor):
    # Dictionary of in-scope variables (environment)
    # env = {}


    def __init__(self):
        super(UniquifyVisitor, self).__init__()

    # Modules
    def visitModule(self, n):
        if(debug):
            print 'in module'
        return Module(n.doc, self.dispatch(n.node,{}), n.lineno)
        # return Module(n.doc, self.dispatch(n.node), n.lineno)

    # Statements
    def visitStmt(self, n, env):
        if(debug):
            print 'in stmt, env = ',env
        nodes = []
        for s in n.nodes:
            nodes += [self.dispatch(s, env)]
        return Stmt(nodes, n.lineno)
    # def visitStmt(self, n):
    #     if(debug):
    #         print 'YAYAYAY'
    #     nodes = []
    #     for s in n.nodes:
    #         nodes += [self.dispatch(s)]
    #     return Stmt(nodes, n.lineno)

    def visitPrintnl(self, n, env):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node,env)]
        return Printnl(nodes, n.dest, n.lineno)

    def visitAssign(self, n, env):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return Assign(nodes, self.dispatch(n.expr, env), n.lineno)
    
    def visitDiscard(self, n, env):
        return Discard(self.dispatch(n.expr, env), n.lineno)
    
    def visitFunction(self, n, env):
        env1 = copy.deepcopy(env)
        return Function(n.decorators, n.name, n.argnames, n.defaults,
                        n.flags, n.doc, self.dispatch(n.code, env1))

    # Terminal Expressions

    def visitConst(self, n, env):
        return Const(n.value, n.lineno)
    

    def visitName(self, n, env):
        return Name(n.name, n.lineno)

    def visitAssName(self, n, env):
        return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitLambda(self, n, env):
        return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code, env))

    def visitReturn(self, n, env):
        return Return(self.dispatch(n.value, env))

    def visitList(self, n, env):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return List(nodes, n.lineno)

    def visitDict(self, n, env):
        items = []
        for item in n.items:
            key = self.dispatch(item[0],env)
            value = self.dispatch(item[1],env)
            items += [(key, value)]
        return Dict(items, n.lineno)

    def visitSubscript(self, n, env):
        expr = self.dispatch(n.expr, env)
        subs = []
        for sub in n.subs:
            subs += [self.dispatch(sub, env)]
        return Subscript(expr, n.flags, subs, n.lineno)
    
    def visitCompare(self, n, env):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1], env))
            ops += [newop]
        return Compare(self.dispatch(n.expr, env), ops, n.lineno)

    def visitAdd(self, n, env):
        return Add((self.dispatch(n.left, env), self.dispatch(n.right, env)), n.lineno)
    
    def visitOr(self, n, env):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return Or(nodes, n.lineno)

    def visitAnd(self, n, env):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return And(nodes, n.lineno)

    def visitNot(self, n, env):
        return Not(self.dispatch(n.expr, env), n.lineno)

    def visitUnarySub(self, n, env):
        return UnarySub(self.dispatch(n.expr, env), n.lineno)

    def visitIfExp(self, n, env):
        return IfExp(self.dispatch(n.test, env),
                     self.dispatch(n.then, env),
                     self.dispatch(n.else_, env),
                     n.lineno)    

    def visitCallFunc(self, n, env):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg, env)]
        return CallFunc(self.dispatch(n.node, env), args, n.star_args, n.dstar_args, n.lineno)



