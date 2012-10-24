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

class EnvFunction(Function):
    def __init__(self, function, env):
        self.function = function
        self.env = env

    def __repr__(self):
        return "EnvFunction(%s, %s)" % (repr(self.function), repr(self.env))

class EnvLambda(Lambda):
    def __init__(self, lambdal, env):
        self.lambdal = lambdal
        self.env = env

    def __repr__(self):
        return "EnvLambda(%s, %s" % (repr(self.function), repr(self.env))


class UniquifyVisitor(CopyVisitor):
    # Dictionary of in-scope variables (environment)
    # env = {}


    def __init__(self):
        super(UniquifyVisitor, self).__init__()

    # Modules
    def visitModule(self, n):
        if(debug):
            print 'in module'
        l_vars = []
        env = {}
        l_vars = self.dispatch(n.node, env, l_vars, True)
        #{Put code here to make dicitonary from l_vars to pass on}
        node = self,dispatch(n.node, env, [], False)
        return Module(n.doc, node, n.lineno)

    # Statements
    def visitStmt(self, n, env, union, collect_pass):
        if(debug):
            print 'in stmt, env = ', env
        if(collect_pass):
            nodes = []   
            for s in n.nodes:
                union += [self.dispatch(s, env, union, collect_pass)]
            return union
        else:
            return Stmt(nodes, n.lineno)

    def visitPrintnl(self, n, env, union, collect_pass):
        if(debug):
            print 'in printnl, env, union = ',env,union
        if(collect_pass):
            for node in n.nodes:
                union += [self.dispatch(node, env, union, collect_pass)]
            return union
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env, union, collect_pass)]
            return Printnl(nodes, n.dest, n.lineno)

    def visitAssign(self, n, env, union, collect_pass):
        if(debug):
            print 'in Assign, env, union =', env,union
        if(collect_pass):
            for node in n.nodes:
                union += [self.dispatch(node, env, union, collect_pass)]
            return union
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env)]
            return Assign(nodes, self.dispatch(n.expr, env, union, collect_pass), n.lineno)
    
    def visitDiscard(self, n, env, union, collect_pass):
        if(debug):
            print 'in Discard, env, union =',env, union
        if(collect_pass):
            union = self.dispatch(n.expr, env, union, collect_pass)
            return union
        else:
            return Discard(self.dispatch(n.expr, env, union, collect_pass), n.lineno)
    
    def visitFunction(self, n, env, union, collect_pass):
        env1 = copy.deepcopy(env)
        l_vars = set([])

        in_scope = self.dispatch(n.code, env1, l_vars)
        return Function(n.decorators, n.name, n.argnames, n.defaults,
                        n.flags, n.doc, in_scope)

    # Terminal Expressions
    def visitConst(self, n, env, union, collect_pass):
        if(debug):
            print 'in Const, env, union =',env, union
        if(collect_pass):
            return union
        else:
            return Const(n.value, n.lineno)
    
    def visitName(self, n, env, union, collect_pass):
        if(debug):
            print 'in Name, env, union =',env, union
        if(collect_pass):
            return union
        else:
            return Name(n.name, n.lineno)

    def visitAssName(self, n, env, union, collect_pass):
        if(debug):
            print 'in AssName, env, union=',env,union
        if(collect_pass):
            union += [n.name]
            return union
        else:
            return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitLambda(self, n, env, union, collect_pass):
        if(debug):
            print 'in Lambda, env, union=',env,union
        if(collect_pass):
            #Start a new union for this function, to collect lhs
            union = []
            union += n.dispatch(n.code, env, union, collect_pass)
            union = set([union])
        else:
            return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code, env, union, collect_pass))

    def visitReturn(self, n, env, union, collect_pass):
        return Return(self.dispatch(n.value, env))

    def visitList(self, n, env, union, collect_pass):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return List(nodes, n.lineno)

    def visitDict(self, n, env, union, collect_pass):
        items = []
        for item in n.items:
            key = self.dispatch(item[0],env)
            value = self.dispatch(item[1],env)
            items += [(key, value)]
        return Dict(items, n.lineno)

    def visitSubscript(self, n, env, union, collect_pass):
        expr = self.dispatch(n.expr, env)
        subs = []
        for sub in n.subs:
            subs += [self.dispatch(sub, env)]
        return Subscript(expr, n.flags, subs, n.lineno)
    
    def visitCompare(self, n, env, union, collect_pass):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1], env))
            ops += [newop]
        return Compare(self.dispatch(n.expr, env), ops, n.lineno)

    def visitAdd(self, n, env, union, collect_pass):
        return Add((self.dispatch(n.left, env), self.dispatch(n.right, env)), n.lineno)
    
    def visitOr(self, n, env, union, collect_pass):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return Or(nodes, n.lineno)

    def visitAnd(self, n, env, union, collect_pass):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node, env)]
        return And(nodes, n.lineno)

    def visitNot(self, n, env, union, collect_pass):
        return Not(self.dispatch(n.expr, env), n.lineno)

    def visitUnarySub(self, n, env, union, collect_pass):
        return UnarySub(self.dispatch(n.expr, env), n.lineno)

    def visitIfExp(self, n, env, union, collect_pass):
        return IfExp(self.dispatch(n.test, env),
                     self.dispatch(n.then, env),
                     self.dispatch(n.else_, env),
                     n.lineno)    

    def visitCallFunc(self, n, env, union, collect_pass):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg, env)]
        return CallFunc(self.dispatch(n.node, env), args, n.star_args, n.dstar_args, n.lineno)

# # Statements
#     def visitStmt(self, n, env, union, collect_pass):
#         if(debug):
#             print 'in stmt, env = ',env
#         if(collect_pass):
#             nodes = []   
#             for s in n.nodes:
#                 nodes += [self.dispatch(s, env, union, collect_pass)]
#         return Stmt(nodes, n.lineno)

#     def visitPrintnl(self, n, env, union, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node,env)]
#         return Printnl(nodes, n.dest, n.lineno)

#     def visitAssign(self, n, env, union, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return Assign(nodes, self.dispatch(n.expr, env), n.lineno)
    
#     def visitDiscard(self, n, env, union, collect_pass):
#         return Discard(self.dispatch(n.expr, env), n.lineno)
    
#     def visitFunction(self, n, env, union, collect_pass):
#         env1 = copy.deepcopy(env)
#         l_vars = set([])

#         in_scope = self.dispatch(n.code, env1, l_vars)
#         return Function(n.decorators, n.name, n.argnames, n.defaults,
#                         n.flags, n.doc, in_scope)

#     # Terminal Expressions
#     def visitConst(self, n, env, union, collect_pass):
#         return Const(n.value, n.lineno)
    

#     def visitName(self, n, env, union, collect_pass):
#         return Name(n.name, n.lineno)

#     def visitAssName(self, n, env, union, collect_pass):
#         return AssName(n.name, n.flags, n.lineno)

#     # Non-Terminal Expressions

#     def visitLambda(self, n, env, union, collect_pass):
#         return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code, env))

#     def visitReturn(self, n, env, union, collect_pass):
#         return Return(self.dispatch(n.value, env))

#     def visitList(self, n, env, union, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return List(nodes, n.lineno)

#     def visitDict(self, n, env, union, collect_pass):
#         items = []
#         for item in n.items:
#             key = self.dispatch(item[0],env)
#             value = self.dispatch(item[1],env)
#             items += [(key, value)]
#         return Dict(items, n.lineno)

#     def visitSubscript(self, n, env, union, collect_pass):
#         expr = self.dispatch(n.expr, env)
#         subs = []
#         for sub in n.subs:
#             subs += [self.dispatch(sub, env)]
#         return Subscript(expr, n.flags, subs, n.lineno)
    
#     def visitCompare(self, n, env, union, collect_pass):
#         ops = []
#         for op in n.ops:
#             newop = (op[0], self.dispatch(op[1], env))
#             ops += [newop]
#         return Compare(self.dispatch(n.expr, env), ops, n.lineno)

#     def visitAdd(self, n, env, union, collect_pass):
#         return Add((self.dispatch(n.left, env), self.dispatch(n.right, env)), n.lineno)
    
#     def visitOr(self, n, env, union, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return Or(nodes, n.lineno)

#     def visitAnd(self, n, env, union, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return And(nodes, n.lineno)

#     def visitNot(self, n, env, union, collect_pass):
#         return Not(self.dispatch(n.expr, env), n.lineno)

#     def visitUnarySub(self, n, env, union, collect_pass):
#         return UnarySub(self.dispatch(n.expr, env), n.lineno)

#     def visitIfExp(self, n, env, union, collect_pass):
#         return IfExp(self.dispatch(n.test, env),
#                      self.dispatch(n.then, env),
#                      self.dispatch(n.else_, env),
#                      n.lineno)    

#     def visitCallFunc(self, n, env, union, collect_pass):
#         args = []
#         for arg in n.args:
#             args += [self.dispatch(arg, env)]
#         return CallFunc(self.dispatch(n.node, env), args, n.star_args, n.dstar_args, n.lineno)


