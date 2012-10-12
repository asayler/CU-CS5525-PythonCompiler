#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# explicate visitor functions
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

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *

class ExplicateVisitor(CopyVisitor):

    # Statements    

    def visitPrintnl(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Printnl(nodes, n.dest, n.lineno)
    
    # Terminal Expressions

    def visitConst(self, n):
        return mono_InjectFrom(INT_t, Const(n.value, n.lineno))

    def visitName(self, n):
        return Name(n.name, n.lineno)

    def visitAssName(self, n):
        return AssName(n.name, n.flags, n.lineno)

    # Non-Terminal Expressions

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)];
        return List(nodes, n.lineno)

    def visitDict(self, n):
        items = []
        for item in n.items:
            items += [self.dispatch(item)];
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
        lhsvar = Name('let_add_lhs')
        rhsvar = Name('let_add_rhs')
        t = mono_Let(lhsvar,
                     self.dispatch(n.left),
                     mono_Let(rhsvar,
                              self.dispatch(n.right),
                              IfExp(And([Or([mono_IsTag(INT_t, lhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)]),
                                         Or([mono_IsTag(INT_t, rhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)])]),
                                    mono_InjectFrom(INT_t, mono_IntAdd((mono_ProjectTo(INT_t,
                                                                                       lhsvar),
                                                                        mono_ProjectTo(INT_t,
                                                                                       rhsvar)))),
                                    IfExp(And([mono_IsTag(BIG_t, lhsvar),
                                               mono_IsTag(BIG_t, rhsvar)]),
                                          mono_InjectFrom(BIG_t, CallFunc(BIGADD_n,
                                                                          [mono_ProjectTo(BIG_t,
                                                                                          lhsvar),
                                                                           mono_ProjectTo(BIG_t,
                                                                                          rhsvar)])),
                                          CallFunc(TERROR_n, [])))))
        return t
        
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
