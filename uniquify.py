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
    def __init__(self, function, env, lvars):
        self.function = function
        self.env = env
        self.lvars = lvars

    def __repr__(self):
        return "EnvFunction(%s, %s, %s)" % (repr(self.function), repr(self.env), repr(self.lvars))

class EnvLambda(Lambda):
    def __init__(self, lambdal, env, lvars):
        self.lambdal = lambdal
        self.env = env
        self.lvars = lvars

    def __repr__(self):
        return "EnvLambda(%s, %s, %s)" % (repr(self.function), repr(self.env), repr(self.lvars))


class UniquifyVisitor(CopyVisitor):
    # Dictionary of in-scope variables (environment)
    # env = {}

    def __init__(self):
        super(UniquifyVisitor, self).__init__()

    # Modules
    def visitModule(self, n):
        if(debug):
            print '\nin module'
        lvars = set([])
        allvars = set([])
        z_vars = [lvars, allvars]
        env = {}
        n, z_vars, all_vars = self.dispatch(n.node, env, lvars, allvars, True)
        #{Put code here to make dicitonary from l_vars to pass on}
        node = self,dispatch(n.node, env, [], False)
        return Module(n.doc, node, n.lineno)

    # Statements
    def visitStmt(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin stmt, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            nodes = []
            n_new = []
            # l = []   
            # r = []
            for s in n.nodes:
                (n_new, l,r) = self.dispatch(s, env, lvars, allvars, collect_pass)
                nodes = n_new
                lvars = lvars | l
                allvars = allvars | r
            return nodes, lvars, allvars
        else:
            return Stmt(nodes, n.lineno)

    def visitPrintnl(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin printnl, n, env, lvars =', env, lvars, allvars
        if(collect_pass):
            nodes = []
            n_new = []
            # l = []
            # r = []
            for node in n.nodes:
                (n_new, l,r) = self.dispatch(n, env, lvars, allvars, collect_pass)
                lvars = lvars | l
                allvars = allvars | r
                nodes += n_new
            return nodes, lvars, allvars
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env, lvars, collect_pass)]
            return Printnl(nodes, n.dest, n.lineno)

    def visitAssign(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Assign, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            nodes = []
            n_new = []
            # l = []
            # r = []
            for node in n.nodes:
                print 'happening once'
                (n_new, l, r) = self.dispatch(node, env, lvars, allvars,collect_pass)
                lvars = lvars | l
                print lvars
                allvars = allvars | r
                print allvars
                nodes += n_new
            return nodes, lvars, allvars
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env)]
            return Assign(nodes, self.dispatch(n.expr, env, lvars, collect_pass), n.lineno)
    
    def visitDiscard(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Discard, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            n, lvars, allvars= self.dispatch(n.expr, env, lvars, collect_pass)
            return n, lvars, allvars
        else:
            return Discard(self.dispatch(n.expr, env, lvars, collect_pass), n.lineno)
    
    def visitFunction(self, n, env, lvars, allvars, collect_pass):
        env1 = copy.deepcopy(env)
        l_vars = set([])
        in_scope = self.dispatch(n.code, env1, l_vars)
        return Function(n.decorators, n.name, n.argnames, n.defaults,
                        n.flags, n.doc, in_scope)

    # Terminal Expressions
    def visitConst(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Const, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            return (n, lvars, allvars)
        else:
            return Const(n.value, n.lineno)
    
    def visitName(self, n, env, lvars, allvars,collect_pass):
        if(debug):
            print '\nin Name, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            #Add to lvars because we want to have a party up in this joint
            #Also we need to keep track of all vars.
            allvars = allvars | [n.name]
            return (n, lvars, allvars)
        else:
            return Name(n.name, n.lineno)

    def visitAssName(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin AssName, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            lvars = lvars | set([n.name])
            allvars = allvars | set([n.name])
            print 'ASSNAME', lvars, allvars
            return (n,lvars, allvars)
        else:
            return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions
    # Be sure to add both parameters and func names
    def visitLambda(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Lambda, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            #Start a new lvars for this function, to collect lhs
            l = set([])
            r = set([])
            for arg in n.argnames: #parameters are new lhs'
                l = l | set([arg])
                r = r | set([arg])
            n, l1, r1 = n.dispatch(n.code, env, l, r, collect_pass)
            l = l | l1
            r = r | r1
            # Put the vars in environment
            this_env = {}
            for var in r:
                this_env[var] = ['']
            new_lambda = EnvLambda(n, this_env, l)
            return new_lambda, lvars, rvars
        else:
            return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code, env, lvars, collect_pass))

    def visitReturn(self, n, env, lvars, allvars, collect_pass):
       if(debug):
            print '\nin Return, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            return n, lvars, rvars
        else:
            return Return(self.dispatch(n.value, env))

    def visitList(self, n, env, lvars, collect_pass):
        if(debug):
            print '\nin List, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            nodes = []
            for node in n.nodes:
                # nodes += [self.dispatch(node, env, lvars, allvars, collect_pass)]
                (n_new, l, r) = self.dispatch(node, env, lvars, allvars,collect_pass)
                lvars = lvars | l
                print lvars
                allvars = allvars | r
                print allvars
                nodes += [n_new]
            return List(nodes, n.lineno), lvars, allvars
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env)]
            return List(nodes, n.lineno)

    def visitDict(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Dict, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            items = []
            for item in n.items:
                key, l, r = self.dispatch(item[0],env, lvars, allvars, collect_pass)
                lvars = l | lvars
                allvars = r | allvars
                value, l, r = self.dispatch(item[1],env, lvars, allvars, collect_pass)
                lvars = l | lvars
                allvars = r | allvars
                items += [(key, value)]
            return Dict(items, n.lineno), lvars, rvars
        else:
            items = []
            for item in n.items:
                key = self.dispatch(item[0],env)
                value = self.dispatch(item[1],env)
                items += [(key, value)]
            return Dict(items, n.lineno)

    def visitSubscript(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Subscript, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            expr = self.dispatch(n.expr, env, lvars, allvars)
            lvars = l | lvars
            allvars = r | allvars
            subs = []
            for sub in n.subs:
                s, l, r = self.dispatch(item[1],env, lvars, allvars, collect_pass)
                lvars = l | lvars
                allvars = r | allvars
                subs += [s]
            return Subscript(expr, n.flags, subs, n.lineno), lvars, allvars
        else:
            expr = self.dispatch(n.expr, env)
            subs = []
            for sub in n.subs:
                subs += [self.dispatch(sub, env)]
            return Subscript(expr, n.flags, subs, n.lineno)
    
    def visitCompare(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Compare, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            ops = []
            for op in n.ops:
                newop, l, r = (op[0], self.dispatch(op[1], env, lvars, allvars, collect_pass))
                lvars = l | lvars
                allvars = r | allvars
                ops += [newop]
            e, l, r = self.dispatch(n.expr, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            return Compare(e, ops, n.lineno), lvars, allvars
        else:
            ops = []
            for op in n.ops:
                newop = (op[0], self.dispatch(op[1], env))
                ops += [newop]
            return Compare(self.dispatch(n.expr, env), ops, n.lineno)

    def visitAdd(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Add, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            left, l, r = self.dispatch(n.left, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            right, l, r = self.dispatch(n.right, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            return Add((left, right), n.lineno), lvars, allvars
        else:
            return Add((self.dispatch(n.left, env), self.dispatch(n.right, env)), n.lineno)
    
    def visitOr(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Lambda, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            nodes = []
            for node in n.nodes:
                n, l, r = self.dispatch(node, env)]
                nodes += [n]
                lvars = l | lvars
                allvars = r | allvars
            return Or(nodes, n.lineno), lvars, allvars
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env)]
            return Or(nodes, n.lineno)

    def visitAnd(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin And, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            nodes = []
            for node in n.nodes:
                n, l, r = self.dispatch(node, env)]
                nodes += [n]
                lvars = l | lvars
                allvars = r | allvars
            return And(nodes, n.lineno), lvars, allvars
        else:
            nodes = []
            for node in n.nodes:
                nodes += [self.dispatch(node, env)]
            return And(nodes, n.lineno)

    def visitNot(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin Not, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            n, l, r = self.dispatch(n.expr, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            return Not(n, n.lineno), lvars, allvars
        else:
            return Not(self.dispatch(n.expr, env), n.lineno)

    def visitUnarySub(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin UnarySub, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            n, l, r = self.dispatch(n.expr, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            return UnarySub(n, n.lineno), lvars, allvars
        else:
            return UnarySub(self.dispatch(n.expr, env), n.lineno)

    def visitIfExp(self, n, env, lvars, allvars, collect_pass):
        if(debug):
            print '\nin IfExp, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            test, l, r = self.dispatch(n.test, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            then, l, r = self.dispatch(n.then, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            else_, l, r = self.dispatch(n.else_, env, lvars, allvars, collect_pass)
            lvars = l | lvars
            allvars = r | allvars
            return IfExp(test, then, else_, n.lineno), lvars, allvars
        else:
            return IfExp(self.dispatch(n.test, env),
                         self.dispatch(n.then, env),
                         self.dispatch(n.else_, env),
                         n.lineno)    

    def visitCallFunc(self, n, env, lvars,allvars, collect_pass):
        if(debug):
            print '\nin CallFunc, n, env, lvars =',n, env, lvars, allvars
        if(collect_pass):
            args = []
            for arg in n.args:
                a, l, r = self.dispatch(arg, env, lvars, allvars, collect_pass)
                lvars = l | lvars
                allvars = r | allvars
                args += [a]
        else:
            args = []
            for arg in n.args:
                args += [self.dispatch(arg, env)]
            return CallFunc(self.dispatch(n.node, env), args, n.star_args, n.dstar_args, n.lineno)

# # Statements
#     def visitStmt(self, n, env, lvars, collect_pass):
#         if(debug):
#             print 'in stmt, env = ',env
#         if(collect_pass):
#             nodes = []   
#             for s in n.nodes:
#                 nodes += [self.dispatch(s, env, lvars, collect_pass)]
#         return Stmt(nodes, n.lineno)

#     def visitPrintnl(self, n, env, lvars, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node,env)]
#         return Printnl(nodes, n.dest, n.lineno)

#     def visitAssign(self, n, env, lvars, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return Assign(nodes, self.dispatch(n.expr, env), n.lineno)
    
#     def visitDiscard(self, n, env, lvars, collect_pass):
#         return Discard(self.dispatch(n.expr, env), n.lineno)
    
#     def visitFunction(self, n, env, lvars, collect_pass):
#         env1 = copy.deepcopy(env)
#         l_vars = set([])

#         in_scope = self.dispatch(n.code, env1, l_vars)
#         return Function(n.decorators, n.name, n.argnames, n.defaults,
#                         n.flags, n.doc, in_scope)

#     # Terminal Expressions
#     def visitConst(self, n, env, lvars, collect_pass):
#         return Const(n.value, n.lineno)
    

#     def visitName(self, n, env, lvars, collect_pass):
#         return Name(n.name, n.lineno)

#     def visitAssName(self, n, env, lvars, collect_pass):
#         return AssName(n.name, n.flags, n.lineno)

#     # Non-Terminal Expressions

#     def visitLambda(self, n, env, lvars, collect_pass):
#         return Lambda(n.argnames, n.defaults, n.flags, self.dispatch(n.code, env))

#     def visitReturn(self, n, env, lvars, collect_pass):
#         return Return(self.dispatch(n.value, env))

#     def visitList(self, n, env, lvars, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return List(nodes, n.lineno)

#     def visitDict(self, n, env, lvars, collect_pass):
#         items = []
#         for item in n.items:
#             key = self.dispatch(item[0],env)
#             value = self.dispatch(item[1],env)
#             items += [(key, value)]
#         return Dict(items, n.lineno)

#     def visitSubscript(self, n, env, lvars, collect_pass):
#         expr = self.dispatch(n.expr, env)
#         subs = []
#         for sub in n.subs:
#             subs += [self.dispatch(sub, env)]
#         return Subscript(expr, n.flags, subs, n.lineno)
    
#     def visitCompare(self, n, env, lvars, collect_pass):
#         ops = []
#         for op in n.ops:
#             newop = (op[0], self.dispatch(op[1], env))
#             ops += [newop]
#         return Compare(self.dispatch(n.expr, env), ops, n.lineno)

#     def visitAdd(self, n, env, lvars, collect_pass):
#         return Add((self.dispatch(n.left, env), self.dispatch(n.right, env)), n.lineno)
    
#     def visitOr(self, n, env, lvars, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return Or(nodes, n.lineno)

#     def visitAnd(self, n, env, lvars, collect_pass):
#         nodes = []
#         for node in n.nodes:
#             nodes += [self.dispatch(node, env)]
#         return And(nodes, n.lineno)

#     def visitNot(self, n, env, lvars, collect_pass):
#         return Not(self.dispatch(n.expr, env), n.lineno)

#     def visitUnarySub(self, n, env, lvars, collect_pass):
#         return UnarySub(self.dispatch(n.expr, env), n.lineno)

#     def visitIfExp(self, n, env, lvars, collect_pass):
#         return IfExp(self.dispatch(n.test, env),
#                      self.dispatch(n.then, env),
#                      self.dispatch(n.else_, env),
#                      n.lineno)    

#     def visitCallFunc(self, n, env, lvars, collect_pass):
#         args = []
#         for arg in n.args:
#             args += [self.dispatch(arg, env)]
#         return CallFunc(self.dispatch(n.node, env), args, n.star_args, n.dstar_args, n.lineno)


