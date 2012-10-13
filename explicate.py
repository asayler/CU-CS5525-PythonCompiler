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

#Reserved Names
TRUENAME   = "True"
TRUEVALUE  = 1
FALSENAME  = "False"
FALSEVALUE = 0

class ExplicateVisitor(CopyVisitor):
    
    # Terminal Expressions

    def visitConst(self, n):
        return mono_InjectFrom(INT_t, Const(n.value, n.lineno))

    def visitName(self, n):
        if(n.name == TRUENAME):
            return mono_InjectFrom(BOOL_t, Const(TRUEVALUE, n.lineno))
        elif(n.name == FALSENAME):
            return mono_InjectFrom(BOOL_t, Const(FALSEVALUE, n.lineno))
        else:
            return Name(n.name, n.lineno)

    # Non-Terminal Expressions

    def visitList(self, n):
        raise Exception("Lists not yet implemented")

    def visitDict(self, n):
        raise Exception("Dicts not yet implemented")

    def visitSubscript(self, n):
        raise Exception("Subscript not yet implemented")
                
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
        
    def visitNot(self, n):
        return Not(self.dispatch(n.expr), n.lineno)

    def visitUnarySub(self, n):
        exprvar = Name('let_us_expr')
        t = mono_Let(exprvar,
                     self.dispatch(n.expr),
                     IfExp(Or([mono_IsTag(INT_t, exprvar),
                               mono_IsTag(BOOL_t, exprvar)]),
                           mono_InjectFrom(INT_t, mono_IntUnarySub(mono_ProjectTo(INT_t, exprvar))),
                           CallFunc(TERROR_n, [])))
        return t

    # Explicate P1 Pyobj functions
    def visitCallFunc(self, n):
        args = []
        # Verify/Rectify Names
        if(isinstance(n.node, Name)):
            name = n.node.name
            if(name == "input"):
                name = "input_int"
            elif(name == "input_int"):
                pass
            else:
                raise Exception("Only input function accepted in p1")
            newName = Name(name)
        else:
            raise Exception("Only named functions accepted in p1")
        #Copy Function
        for arg in n.args:
            args += [self.dispatch(arg)]
        return CallFunc(newName, args, n.star_args, n.dstar_args, n.lineno)
